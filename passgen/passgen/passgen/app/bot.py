from aiogram import Bot, Dispatcher, executor, types
from passgen.util import get_config_from_yaml
from passgen.core import (
    PasswordServiceImpl,
    PassIdGeneratorServiceImpl,
    PasswordGeneratorServiceImpl,
    PasswordSpec,
    PassIdSpec,
    Password
)
from passgen.integrations import DatabasePasswordStorage
from passgen.integrations.pass_storage.models.base import Base
from sqlalchemy import create_engine

config = get_config_from_yaml("config/config.yaml")
engine = create_engine(config.integrations.pass_storage.sync_url)
Base.metadata.create_all(engine)

bot = Bot(token=config.bot.token)
dp = Dispatcher(bot)

# dependency injection aiogram?
pass_storage = DatabasePasswordStorage(config.integrations.pass_storage)
pass_svc = PasswordServiceImpl(pass_storage)
passgen_svc = PasswordGeneratorServiceImpl()
pass_idgen_svc = PassIdGeneratorServiceImpl()


def format_password(p: Password) -> str:
    return f"{p.label} : {p.password}\nCreated at: {p.created_at}\nPhrase: {p.phrase}"


# password complexities
password_level_specs = {
    "easy": PasswordSpec(use_ascii=True, use_digits=True,
                         use_special=False, length=8),
    "medium": PasswordSpec(use_ascii=True, use_digits=True,
                           use_special=False, length=12),
    "hard": PasswordSpec(use_ascii=True, use_digits=True,
                         use_special=True, length=16)
}


@dp.message_handler(commands=['start', 'help'])
async def send_start(message: types.Message):
    await message.reply("Hi!\nI'm KreschPasswordBot!\n"
                        "My creation was budgeted at two beers")


@dp.message_handler(commands=['new', 'generate', 'create', 'register'])
async def generate_password(message: types.Message):
    arg = message.get_args().lower()
    if not arg:
        await message.reply("You must provide exactly 1 argument: "
                            "complexity level, one of [easy, medium, hard]")
        return

    if arg not in password_level_specs:
        await message.reply("You provided wrong password complexity")
        return
    spec = password_level_specs[arg]

    password = passgen_svc.generate(spec)
    await message.reply(f"Your password: {password}\n"
                        "If you want to save it, reply this message with desired label.\n"
                        "You'll see passphrase which you can use to share credentials with somebody or to get from another account")


@dp.message_handler(commands=['list'])
async def show_passwords_list(message: types.Message):
    owner = str(message.from_id)
    password_list = await pass_svc.from_owner(owner)
    msg_password_list = [format_password(p[0]) for p in password_list]
    await message.reply("\n\n".join(msg_password_list))


@dp.message_handler(commands=['phrase'])
async def get_pass_by_phrase(message: types.Message):
    phrase = message.get_args()
    pass_ = await pass_svc.from_phrase(phrase)
    if pass_ is None:
        await message.reply("Password not found")
        return
    await message.reply(format_password(pass_))


@dp.message_handler(commands=['delete'])
async def delete_pass(message: types.Message):
    label = message.get_args()
    owner = str(message.from_id)
    is_deleted = await pass_svc.delete_password(label, owner)
    if is_deleted:
        await message.reply("Successfully deleted")
    else:
        await message.reply("Failed to delete")


@dp.message_handler(commands=['new_phrase'])
async def update_phrase(message: types.Message):
    label = message.get_args()
    owner = str(message.from_id)
    phrase = pass_idgen_svc.generate(PassIdSpec(length=5))
    is_updated = await pass_svc.set_phrase(phrase, label, owner)
    if is_updated:
        await message.reply(f"New phrase: {phrase}")
    else:
        await message.reply("Failed to update")


@dp.message_handler()
async def save_password(message: types.Message):
    label = message.text
    if not label:
        await message.reply("You must provide label for this password")
        return
    if message.reply_to_message is None:
        return
    msg = message.reply_to_message.text
    if not msg.startswith("Your password: "):
        return
    password = "".join(msg.split()[2:3])
    phrase = pass_idgen_svc.generate(PassIdSpec(length=5))
    owner = str(message.from_id)
    is_saved = await pass_svc.save_password(owner, label, phrase, password)
    if is_saved:
        await message.reply(f"Saved password {password}\n"
                            f"Label: {label}\n"
                            f"Phrase: {phrase}")
    else:
        await message.reply("Password with this label already exist!"
                            "Choose another label")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
