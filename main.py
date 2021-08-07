# -*- coding: utf-8 -*-


# ------------- УСТАНАВЛИВАЕМ НУЖНЫЕ МОДУЛИ
# pip install -u discord.py
# pip install -u stdout
# pip install -u aiosqlite
# pip install -u discord-py-slash-command


# ------------- ИМПОРТ МОДУЛЕЙ

import logging  # Импортируем модуль логирования

import aiosqlite  # Импортируем модуль работы с базами SQLite
import discord  # Импортируем основной модуль
from discord.ext import commands  # Импортируем команды из модуля discord.ext
from discord_slash import SlashCommand, SlashContext  # Импортируем модуль команд с косой чертой (slash)
from discord_slash.utils.manage_commands import create_choice, create_option

import config  # Импортируем настройки приложения


# ------------- ИМПОРТ МОДУЛЕЙ // КОНЕЦ


# ------------- СОЗДАЁМ ПРИЛОЖЕНИЕ И НАЗЫВАЕМ ЕГО CLIENT
client = commands.Bot(description=config.client_short_description, command_prefix=None, help_command=None)


# ------------- СОЗДАЁМ ОБРАБОТКУ КОМАНДЫ С КОСОЙ ЧЕРТОЙ ЧЕРЕЗ СОЗДАННОЕ ПРИЛОЖЕНИЕ
slash = SlashCommand(client, sync_commands=True)


# ------------- СОЗДАЁМ ОБРАБОТКУ КОМАНДЫ С КОСОЙ ЧЕРТОЙ ЧЕРЕЗ СОЗДАННОЕ ПРИЛОЖЕНИЕ // КОНЕЦ


# ------------- РЕГИСТРИРУЕМ СОБЫТИЯ ПРИЛОЖЕНИЯ
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(process)d:%(thread)d: %(module)s:%(lineno)d: %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# ------------- РЕГИСТРИРУЕМ СОБЫТИЯ ПРИЛОЖЕНИЯ // КОНЕЦ


# ------------- СОЗДАЁМ ШАБЛОН С ССЫЛКОЙ ДЛЯ ПОДКЛЮЧЕНИЯ ПРИЛОЖЕНИЯ К СЕРВЕРУ
def get_invite_link(bot_id):
    return f'https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot%20applications.commands'  # noqa: E501


# ------------- СОЗДАЁМ ШАБЛОН С ССЫЛКОЙ ДЛЯ ПОДКЛЮЧЕНИЯ ПРИЛОЖЕНИЯ К СЕРВЕРУ // КОНЕЦ


# ------------- ВЫВОДИМ ДАННЫЕ ПРИЛОЖЕНИЯ ПРИ ПОДКЛЮЧЕНИЕ В КОНСОЛЬ
@client.event
async def on_ready():
    client.sql_conn = await aiosqlite.connect(config.db_file_name)
    await client.sql_conn.execute('create table if not exists black_list (userid integer not null unique, '
                                  'add_timestamp text default current_timestamp, reason text, banner_id integer);')

    # Показывает имя приложения, указанное на discordapp.com
    logger.info(f'APP Username: {client.user} ')
    logger.info(f'Using token {config.token[0:2]}...{config.token[-3:-1]}')

    # Показывает ID приложения указанное на discordapp.com
    logger.info('APP Client ID: {0.user.id} '.format(client))
    logger.info(f'Link for connection: {get_invite_link(client.user.id)}')

    # Выводит список серверов, к которым подключено приложение
    logger.info('Servers connected to: ' + ''.join('"' + guild.name + '"; ' for guild in client.guilds))

    # Изменяем статус приложения
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Elite Dangerous'))


# ------------- ВЫВОДИМ ДАННЫЕ ПРИЛОЖЕНИЯ ПРИ ПОДКЛЮЧЕНИЕ В КОНСОЛЬ // КОНЕЦ


# ------------- ВЫВОДИМ СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЕЙ В КОНСОЛЬ ПРИЛОЖЕНИЯ
@client.event
async def on_message(message):
    # Игнорируем сообщения, отправленные этим приложением
    if message.author.id == client.user.id:
        return

    # Console Log // Выводим сообщения пользователей в консоль Python
    logger.info('Message: {0.guild} / #{0.channel} / {0.author}: {0.content}'.format(message))

    # Игнорируем сообщения в ЛС
    if isinstance(message.channel, discord.DMChannel):
        return

    # Игнорируем сообщения, отправленные другими приложениями
    if message.author.bot:
        return


# ------------- ВЫВОДИМ СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЕЙ В КОНСОЛЬ ПРИЛОЖЕНИЯ // КОНЕЦ


# ------------- РЕГИСТРИРУЕМ КОМАНДЫ С КОСОЙ ЧЕРТОЙ
@client.event
async def on_slash_command(ctx):
    logger.info(f'Got slash command; {ctx.guild} / {ctx.author} / command: {ctx.name};'
                f' subcommand_name: {ctx.subcommand_name};'
                f' subcommand_group: {ctx.subcommand_group}; options: {ctx.data.get("options")}')


# ------------- РЕГИСТРИРУЕМ КОМАНДЫ С КОСОЙ ЧЕРТОЙ // КОНЕЦ


# ------------- РЕГИСТРИРУЕМ ОШИБКИ КОМАНД С КОСОЙ ЧЕРТОЙ И СООБЩАЕМ ОБ ЭТОМ ПОЛЬЗОВАТЕЛЯМ
@client.event
async def on_slash_command_error(ctx, error):
    logger.warning(
        f"An error occurred: {ctx.guild} / {ctx.author} / command: {ctx.name}; Error: {error}")
    if isinstance(error, discord.ext.commands.NotOwner):
        # Создаём информационное сообщение
        emSlashErrorNotOwner = discord.Embed(title='ВНИМАНИЕ!', description=ctx.author.mention + ', выполнение этой команды доступно только владельцу приложения.', color=0xd40000)
        # Отправляем информационное сообщение и удаляем его через 13 секунд
        await ctx.send(embed=emSlashErrorNotOwner, delete_after=13)
        return

    await ctx.send(str(error), delete_after=13)


# ------------- РЕГИСТРИРУЕМ ОШИБКИ КОМАНД С КОСОЙ ЧЕРТОЙ И СООБЩАЕМ ОБ ЭТОМ ПОЛЬЗОВАТЕЛЯМ // КОНЕЦ


# ------------- КОМАНДА ПРОВЕРКА ПРИЛОЖЕНИЯ
@slash.slash(name="ping", description='Проверить состояние приложения.')
# Команду может выполнить только владелец приложения
@commands.is_owner()
async def ping(ctx):
    # Создаём информационное сообщение
    emPing = discord.Embed(title='⚠ • ВНИМАНИЕ!', description='Получен ответ.', colour=0x2F3136)
    # Отправляем информационное сообщение и удаляем его через 13 секунд
    await ctx.send(embed=emPing, delete_after=13)


# ------------- КОМАНДА ПРОВЕРКА ПРИЛОЖЕНИЯ // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ ИНФОРМАЦИИ О ПРИЛОЖЕНИИ
@slash.slash(name="information", description="Показать информацию о приложение",)
async def information(ctx):
    # Создаём сообщение
    emInformation = discord.Embed(title='ИНФОРМАЦИЯ',
                                  description=config.client_full_description.format(
                                      invite_link=get_invite_link(client.user.id)),
                                  colour=0x2F3136)
    emInformation.add_field(name='Разработчики', value='• <@420130693696323585>\n• <@665018860587450388>')
    emInformation.add_field(name='Благодарности', value='• <@478527700710195203>')
    # emInformation.add_field(name='Список серверов', value="".join(guild.name + '\n' for guild in client.guilds))
    emInformation.set_footer(text=client.user.name)
    # Отправляем сообщение и удаляем его через 60 секунд
    await ctx.send(embed=emInformation, delete_after=60)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ ИФОРМАЦИИ О ПРИЛОЖЕНИЕ // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СПИСКА ВСЕХ КОМАНД ДЛЯ ВЫЗОВА СБОРОК ПО КОРАБЛЯМ
@slash.subcommand(
    base='ships',
    name='show',
    base_desc='Сборки по кораблям',
    description='Список команд для вызова сборок по кораблям.'
)
async def ships_show(ctx):
    # Создаём сообщение
    emShipsShow = discord.Embed(title='СПИСОК КОМАНД ПО КОРАБЛЯМ', description='Список всех сборок кораблей которые на данный момент доступны у бота.', colour=0x2F3136)
    emShipsShow.add_field(name='Малые', value='• Adder\n• Cobra MkIII `/cobramk3`\n• Cobra MkIV\n• Diamondback Explorer `/dbe`\n• Diamondback Scout\n• Dolphin\n• Eagle\n• Hauler\n• Imperial Courier `/courier`\n• Imperial Eagle\n• Sidewinder `/sidewinder`\n• Viper\n• Viper MkIV\n• Vulture `/vulture`')
    emShipsShow.add_field(name='Средние', value='• Alliance Challenger `/challenger`\n• Alliance Chieftain `/chieftain`\n• Alliance Crusader `/crusader`\n• Asp Explorer `/aspe`\n• Asp Scout\n• Federal Assault Ship `/fas`\n• Federal Dropship\n• Federal Gunship\n• Fer-de-Lance `/fdl`\n• Keelback\n• Krait MkII `/krait`\n• Krait Phantom `/phantom`\n• Mamba `/mamba`\n• Python `/python`\n• Type-6 Transporter `/type6`')
    emShipsShow.add_field(name='Большие', value='• Anaconda `/anaconda`\n• Beluga Liner\n• Federal Corvette `/corvette`\n• Imperial Clipper\n• Imperial Cutter `/cutter`\n• Orca\n• Type-7 Transporter `/type7`\n• Type-9 Heavy `/type9`\n• Type-10 Defender `/type10`', inline=False)
    emShipsShow.set_footer(text=client.user.name)
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(embed=emShipsShow, delete_after=300)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СПИСКА ВСЕХ КОМАНД ДЛЯ ВЫЗОВА СБОРОК ПО КОРАБЛЯМ // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Cobra Mk III
@slash.subcommand(
    base='ships',
    name='cobramk3',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Cobra Mk III»'
)
async def cobramk3(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/cobramk3.png", filename="cobramk3.png')
    # Создаём сообщение
    emShipsCobraMK3 = discord.Embed(title='Cobra Mk III', description='Настоящий многофункциональный корабль. Cobra Mk III отлично подходит для целевого спектра задач. В бою он способен нанести ощутимый урон и при необходимости может быстро покинуть сражение, а его просторный трюм позволяет перевозить большой объём грузов, чем другие корабли сходного размера и ценовой категории. Cobra также отлично подходит для исследователей благодаря своему вместительному топливному баку и шести внутренним отделениям.', colour=0x2F3136)
    emShipsCobraMK3.add_field(name='CMDR GIF Community', value='n/a')
    emShipsCobraMK3.add_field(name='Dark Enterprise', value='• [Cobra MK III Универсальная](https://s.orbis.zone/7sa9)\n• Автор: <@461538602715971594>\n\n• [Кобра без орудий для путешествий](https://s.orbis.zone/1slr)\n• Автор: <@270156067055468544>\n\n• [Кобра исследователь](https://s.orbis.zone/2tf3)\n• Автор: Andrew An\n\n• [Быстрая Кобра (Boost 608 m/s)](https://s.orbis.zone/2_xu)\n• Автор: <@189334900405436416>')
    emShipsCobraMK3.set_thumbnail(url='attachment://cobramk3.png')
    emShipsCobraMK3.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsCobraMK3, delete_after=300)

    # Dark Enterprise
    # Cobra MK III Универсальная - https://s.orbis.zone/7sa9 /----/ https://coriolis.io/outfit/cobra_mk_iii?code=A2pataFalddasaf427270p0p04043245030101v6002i.Iw1%2FgDJQ.Aw18cQ%3D%3D.H4sIAAAAAAAAA42Rr0sEURSFz87ujDu%2FHGfdWQcFQXfUZjNsEZsWQbBsEcxi2CBYNmgzGEQEwWQwGoyGjf4BRoOI0aAmk67veu7CPow74ePw7jf3ce%2BDGQPw6xL9cyLsOUB8FAFpm6l2HwLFVwmQklm1Zpeobv2IJK%2FLQOOuQvORjcQxDSsdEEnxLVJ%2FJ7LrBMjVbHamaJbNtDUPh%2Bbguno3o%2FnMirimZaVjwo%2BMSHCRAnOa5jUtaFrUJFXTtjonQEV7uu0ZwLuNefGgpz%2BKFJhtK80S7q7P%2Bv6nSL72IdI8exORcBQpMutWutIF33gcVneXasof%2BE%2BhSWKzYc1LNTscLFUUpwHridm09T3Cyfsinm40bJX5Xi9E9jTOdj19iszsDPXaxBKwcjLJU8H%2F7w%2Fx1ksa%2FgEAAA%3D%3D.EweloBhBGA2EAcICmBDA5gG2SGF8hRFA&bn=Cobra%20Universal
    # Кобра без орудий для путешествий - https://s.orbis.zone/1slr /----/ https://coriolis.io/outfit/cobra_mk_iii?code=A0pdtdFaldddsdf4----02-33450301v62i.Iw1%2FkA%3D%3D.Aw1%2FkA%3D%3D..EweloBhBGA2MoFMCGBzANokMK5FAoA%3D%3D&bn=Cobra%20PVE
    # Кобра исследователь - https://s.orbis.zone/2tf3 /----/ https://coriolis.io/outfit/cobra_mk_iii?code=A0p8tdFaldd3sdf4------321P480d2iv6.Iw18gDCQ.Aw1%2FkA%3D%3D.H4sIAAAAAAAAA1WPOw4BURiFj%2Fc7wxiP6Lw7odCIxAYsQCOxBBoUEgqF2gqUSqVCoVBagogFKBSiEP7ff8XcxBRfJjnfPfdckA%2FA2yN4LQWhnROIzMJArCN%2F5jYEFO4OgB3U0uZU4D8EAKP5YE6uDMmdlNT5UGAUnszWVZBQeXrjBvL9lJguymhzZJvfm6xJQsyTJOymmi0Z46vkxzMze6ihj84FAVUYrMaArCrJKRQVSmES3Uu9%2F5L9hbmiNnOU2rppgN9LTCVZ67dsViPSvZuYJnVt04yWgfoiLvsY9vcBK1p89EMBAAA%3D.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=Cobra%20explorer
    # Быстрая Кобра (Boost 608 m/s) - https://s.orbis.zone/2_xu /-----/ https://coriolis.io/outfit/cobra_mk_iii?code=A4pataFaladasaf427270p0p0404322bB3v6m3m32525.Iw1%2FgDJQ.IzAM4yLUXI%3D%3D.H4sIAAAAAAAAA42RO0sDQRSFbx67JNkkmyx5%2BUDUrBaidhaCaCmIiGBhQAvtRBsLiyDaWdiJjYWVgqWFpaWFf8FKC2sfCBKCaDLHc4Vd0SpbHM7O%2FeaemTtibBFpW5TWEcW7fwIyaQPkl%2BMifldCxDmnQ8TMKBlRcp%2FiKlS6YinR4CKiphR22tG6%2FwlUtF7o%2BwKKx65IdbtMMma6Q7KumddOgD9wsbBXJGSZyQAa0qThlZxIUl1K3YC6QXWwzVpAejePgFt%2FAcanmgASphYmxShWrUfEvszwJJoUX2Umkp1AKbMUQJWDBmDt0tobH0D18BkoZ3UEzi%2Fkzbd5nQklX6Mk595Jrr%2BR3OIv0mY2zDzVYS1yRJXbpEj%2Bgg%2FiqzgqyHRMumYsJE8o2SZnnx9tAf40L%2BOoQ84shNCmtjvjs%2FBEJLWx%2F%2FNABTPyp5NzR5vt7yWkztM9vjoUOyYh%2F75vsJ9Vm3oCAAA%3D.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=Valor%20(Fast%20PVE)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Cobra Mk III // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Cobra MkIV
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Cobra MkIV // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Diamondback Explorer
@slash.subcommand(
    base='ships',
    name='dbe',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Diamondback Explorer»'
)
async def dbe(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/diamondbackexplorer.png", filename="dbe.png')
    # Создаём сообщение
    emShipsDBE = discord.Embed(title='Diamondback Explorer', description='Более крупный собрат Diamondback Scout, также представляет собой корабль двойного назначения, ориентированный на бои и исследования. Выдающаяся огневая мощь и система гнёзд Explorer делают более универсальным по сравнению со Scout, а большая дальность прыжка и превосходная теплоэффективность отлично подойдут исследователям.', colour=0x2F3136)
    emShipsDBE.add_field(name='CMDR GIF Community', value='• [DBE за 77](https://s.orbis.zone/czgy)\n• Автор: <@184299323624783872>')
    emShipsDBE.add_field(name='Dark Enterprise', value='• [DBE Explorer](https://s.orbis.zone/qov)\n• Автор: <@189334900405436416>\n\n• [DBE Explorer 71.80 прыжок](https://s.orbis.zone/2wux)\n• Автор: <@269516916631142411>')
    emShipsDBE.set_thumbnail(url='attachment://dbe.png')
    emShipsDBE.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsDBE, delete_after=300)

    # CMDR GIF Community
    # DBE за 77 - https://s.orbis.zone/czgy /-----/ https://coriolis.io/outfit/diamondback_explorer?code=A0p0tdFfldd3sdf4-------321P0i43v61y9q2i.Iw18SQ%3D%3D.Aw18SQ%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8Zw9XWQ8kOI5wMjDw23z7%2F19sAT9QnumfGFy%2BDEjwq%2Fz6%2F19E7vf%2F%2F6IgeYkNLAwMygXiQJXM%2F6TgKitgKsE2iURIA1XeAcr8Z%2FlnCFPEX%2FEGKH%2Fm3v%2F%2F%2F1n%2FWcG1tgAJTpCBXAaCDAyKIEOUQIQqiFDj%2BQdUzvYvAdWQAw%2F%2B%2F9cDufm%2F0D8fuEmFDFCfCIEUiaz4C3QzyBESCR%2BAKsX%2BxcJUCgmoMzCYdggD3fefAQYATsmgtEMBAAA%3D.EwegLCAMUgjAbCUBTAhgcwDbJHS%2BZpIg

    # Dark Enterprise
    # DBE Explorer - https://s.orbis.zone/qov /-----/ https://coriolis.io/outfit/diamondback_explorer?code=A0p0tdFfldd3sdf4-------1P3243v62i2f.Iw1%2FADGQ.Aw18UA%3D%3D.H4sIAAAAAAAAAz2OvQ7BYBSGT6sVf0m1isYi%2FjdhFQmjwT1wCSzSgXtwGUaDwehCDGI2GBqD6DnOm6hvePPlPM%2BbcwyeEFFsaHx2GplIv06BRSpHi0hMDsBN8I2Gs1LkI8q%2BTRTsVW%2FNIhFJcQ2mDTOE2X6LeOc8kb8tq3lVIhYPIVngy6fy012rNo%2BSanZVJcoNXKIG%2Bk1EB9HFTZLmZWI64UP7l5tIf%2FxS5PL8v38NjqkHyT%2FEei72B9gpJV4kplfsEQ2ndT1N6Pe%2Br5CN6xMBAAA%3D.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=DBE%20Explorer
    # DBE Explorer 71.80 прыжок - https://s.orbis.zone/2wux /-----/ https://coriolis.io/outfit/diamondback_explorer?code=A0p0tdFfldd3sdf4---02---1P32430i0Vv69q2i.Iw1%2BgDC1A%3D%3D%3D.Aw18SQ%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8ZwdXWQ8kOAJ%2B%2F%2F%2FP%2F0CPgUFsAwtQ5QWgQf%2BZ%2FonBFZUBCX6VX%2F%2F%2Fi7wBEqIL%2BBkYJEAqlQvEgSqZ%2F0nBVVbAVIKtE6kRBaq8A5T5z%2FLPEKSIBSSf8AEov%2BXR%2F%2F%2F%2FWf9ZwbU2AAlOkIFcBoIMDIogQ5RAhCqIUOP5B1TO9i8Bppy%2F4g3QkAMP%2Fv%2FXs%2FkGlOL%2Bp4YqdeYeUFTwnw%2Fc%2FByQFEitEEheZMVfoE9ATpMAOee%2F2L9YmEohAXUGBtMOYaCr%2FzPAAQDt0L78XwEAAA%3D%3D.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=DBE%20Jumpy


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Diamondback Explorer // КОНЕЦ

# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Diamondback Scout
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Diamondback Scout // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Dolphin
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Dolphin // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Hauler
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Hauler // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Courier
@slash.subcommand(
    base='ships',
    name='courier',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Imperial Courier»'
)
async def courier(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/imperialcourier.png', filename='courier.png')
    # Создаём сообщение
    emShipsCourier = discord.Embed(title='Imperial Courier', description='Одно из самых компанктных судов на рынке, Imperial Courier представляет собой лёгкий боевой корабль от Gutamaya. Он может похвастаться маневренностью, которая составит конкуренцию даже Viper MkIII, и способен с лёгкостью уходить от огня противника, в то время как три средних гнезда сделали его популярным среди пилотов, ищущих хорошее сочетание силы и стиля.', colour=0x2F3136)
    emShipsCourier.add_field(name='CMDR GIF Community', value='• [Скоростной для планетарных операций](https://s.orbis.zone/cdx_)\n• Авторы: <@232550259841171466>')
    emShipsCourier.add_field(name='Dark Enterprise', value='• [Быстрый курьер](https://s.orbis.zone/3z6y)\n• [Боевой курьер с призмой](https://s.orbis.zone/71hp)\n• Автор: <@270156067055468544>\n\n• [Курьер Быстрый Боевой](https://s.orbis.zone/2jf5)\n• Автор: <@189334900405436416>\n\n• [Исследовательский курьер](https://s.orbis.zone/3d64)\n• Автор: Andrew An\n\n• [Торпедный курьер](https://s.orbis.zone/80tV)\n• Автор: <@514930529183989842>')
    emShipsCourier.set_thumbnail(url='attachment://courier.png')
    emShipsCourier.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsCourier, delete_after=300)

    # CMDR GIF Community
    # Скоростной для планетарных операций - https://s.orbis.zone/cdx_ /-----/ https://coriolis.io/outfit/imperial_courier?code=A0p0tzF5l3dds8f3--2a----2t1N3uv6011y2i3w.Iw1%2BgDGQ.Aw18IwgTKFA%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8ZwdXWQMkOAJ%2B%2F%2F%2FP%2F0CPgUFsAwtQ5QWgQf%2BZ%2FonBFRUDCX6VX%2F%2F%2Fi8gBVYou4GdgkACpVC4QB6pk%2FicFV1kBUwm2TqRGFKjyDlDmP8s%2FQ5gi%2Foo3QPkz9%2F7%2F%2F8%2F6zxKutQlIcPL8%2B%2F%2Bfa4ogA4MiiKUEYqmCWGog1n%2B2fwmohhx48P%2B%2Fns03oElc%2F8LgJqUBCbaQT0A%2FTXgBVHTjzv%2F%2FEgkfgIoE%2F%2FnBFeWADAH5RBDkexWwT0T%2FxcLkhQTUGRhMO4SBov8Z4AAARAmD0GQBAAA%3D.IwegLCoAwgHOICmBDA5gG0SSVchgUA%3D%3D&bn=Superbolide

    # Dark Enterprise
    # Быстрый курьер - https://s.orbis.zone/3z6y /-----/ https://coriolis.io/outfit/imperial_courier?code=A0p8tzF5l3dds8f2---02---2t1N3uv6242i3w-.Iw18QDJQ.Aw18SQ%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8Zw9XWQ8kOI5wMjDw23z7%2F19sAT9QnumfGFy%2BBEjwq%2Fz6%2F1%2FkDZAQBclLbGBhYFAuEAeqZP4nBVdZDlMJtkmkRhSo8g5Q5j%2FLP0OYIv6KN0D5M%2Ff%2B%2F%2F%2FP%2Bs8SrrUFSHDy%2FPv%2Fn2uKIAODIoilBGKpglhqINZ%2Ftn8JqIYcePD%2Fvx7Izf%2B5%2F6mBpBhBUhJ%2FgFI574Cigv984OYXMkD9JwTSKrLiL9AnIKdJJHwAqhT5FwtSCfQUg5CDPAODKTgQ%2FjPAAQAtuxh%2BWgEAAA%3D%3D.EwegLCAMXjCmBDA5gGziEBGSObUkA%3D%3D%3D&bn=Courier%20Roket
    # Боевой курьер с призмой - https://s.orbis.zone/71hp /-----/ https://coriolis.io/outfit/imperial_courier?code=A0p5tzF8l3das8f227272708080808402t1E1E27252525.Iw18SQ%3D%3D.Aw18SQ%3D%3D.H4sIAAAAAAAAA42SP0vDUBTFb9Mmtn1pQmJTi4p%2Fo6CD1LEgOAku7h39AA4FEToI6u4k4uTQD%2BDg6NDBwdFVcJDiB3AUEa33em6hD4qDyXA45Pxy373vhniCiH5cyOACYnoOUeXUJ4pacPGdIUrfc0SS421LnkCKDyWicOtDpNYNkTtcs%2FkhJEy%2FRKpz3yKJ5vXbAtFyewpknqct2RmRw5OqxwnIFyRS4M0RFHbekD%2F2RcTlpv30DFLyWaR8GREtqltSt6JuVZ14vD9e5P5VZEN7liK3bCVMSwVtwm3NEHk3FXQ6bKKUBSpngQzvWOha29G3ceMI4%2Bo9zj8HgPwsUIV3xyDTxriRSnpeRh78k4e8Z%2FMDiFMfiHi6HdPMY%2B19SKInpT38GjLJaxa%2FggSNT9xjV6%2BwyutjkXmCDRZmUURdrGtP1UmSmaxlJoX%2BPr%2FzFR%2BFzgIAAA%3D%3D.CwegjOIAwgTNICmBDA5gG0ScVcJlEA%3D%3D&bn=Multi%20PvE%20Courier
    # Курьер Быстрый Боевой - https://s.orbis.zone/2jf5 /-----/ https://coriolis.io/outfit/imperial_courier?code=A0p5tzF5l3das8f2PhihPh080h00032tB41E276e2E.Iw18UA%3D%3D.IwBj4jQo.H4sIAAAAAAAAA3WRMUsDQRCFR70kl9xdLjkvMQQbNSo2QSGNINYWghZincbGSrAR0UKwtBAx2Ka0tLCw9AdYWFoECVYiKcRCRM2Mb05uiZJs8Rhmvp2ZfUucJKJuAvJ9BnFqNpHnskjeThEFxy8ilRbKMsTLhjyE2OtfIn67SlS8skDeA5dhLhpoF%2BJXPkXCDqTQ9IlKSk7tjIEc4bIh92MyuHGIwoMCyGimxQsKWVqvv6J%2B%2FSQiCV40V48gaV03c54nmtBoUqNpjWY0kiTXY9zf66DJbVukuvSOTjZvmk45SHLjDW86fQb00BIp6UxJ90Bbg6BMD5QaBDm8YqALNTvyWaVyksGmLq%2F93fTuEbc89vpks1zrk83xqpmwrSV9ZqD18LKLT1BXf3cJeM6QDUh2%2FgPJproyyuOx625uFhf068qRYUL%2Fzw%2FOdm4nQQIAAA%3D%3D.IwOgrA9AzBqQDBALBRBTAhgcwDZorPEaifEA&bn=Speed%20Wagon
    # Исследовательский курьер - https://s.orbis.zone/3d64 /-----/ https://coriolis.io/outfit/imperial_courier?code=A0p3t3F5l3d3s8f3-------2t1N3u0d0d-2i24.Iw1%2BgDNJA%3D%3D%3D.Aw18SQ%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8Zw9XWQ8kOI5wMjDw23z7%2F19sAT9QnumfGFy%2BDEjwq%2Fz6%2F1%2FkDZAQBclLbGBhYFAuEAeqZP4nBVdZDlMJtkmkRhSo8g5Q5j%2FLP0OYIv6KN0D5M%2Ff%2B%2F%2F%2FP%2Bs8KrrUFSHCCDOQyEGRgUAQZogQiVEGEGs8%2FoHK2fwmohhx48P%2B%2FHsjN%2FwX%2F%2BcBNKmSA%2BkQIpEhkxV%2Bgm0GOkEj4AFQp%2Bi8WplJIQJ2BwbRDGOi%2B%2FwwwAADlqaarQwEAAA%3D%3D.EweloBhAOEoUwIYHMA28QgIwV3fEQA%3D%3D&bn=%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9%20%D0%BA%D1%83%D1%80%D1%8C%D0%B5%D1%80
    # Торпедный курьер - https://s.orbis.zone/80tV /-----/ https://coriolis.io/outfit/imperial_courier?code=A00BtzF3l3dds8f12i2i2i020404044001010027082j3x.Iw18SQ%3D%3D.EwBj4yIRlI%3D%3D.H4sIAAAAAAAAA42Rv0vDUBDHr7%2BiSdqElxqNIKL26eBQdLS46yI4iHMH%2F4CCS3F27ODs5OAf4B%2Fg4OCo4NihFMcOHaRDB613fg9JICDYDB%2BOd5%2B7e7lHvEBE3wXA7wG1hzKR6SKKRiUie4FIirysUgWYXQKh%2FRRZWv8Sie9CokRrGp0VmCVezcwroPD0LvKrD3DYeMM0KfN%2BKoXdsUj0MhSRCrey0mvA1YbeniHa1PotxbZip8rQHW7nm%2Bik5uEUqUU%2BzzrFgHM2wSVuRpD6A5Gk%2FQHJnUfy5pF8dv%2F4nSofZ6W3ut0Obm0UtudhCbV%2F8gEf5fP3DvqfYudGo%2BQZQ61GEvJJahaTGTajz%2BEf4PXMEIj7AcxHXXydd1PTfwWDjTVIGkX6jlYjEcp%2FPyTZEmwiAgAA.EweloBjEEYoUwIYHMA28SwtkU9A%3D&bn=Sonic%20run!%20v1.1


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Courier// КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Eagle
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Eagle // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Sidewinder
@slash.subcommand(
    base='ships',
    name='sidewinder',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Sidewinder»'
)
async def sidewinder(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/sidewinder.png', filename='sidewinder.png')
    # Создаём сообщение
    emShipsSidewinder = discord.Embed(title='Sidewinder', description='Многоцелевой корабль производства Faulcon DeLacy. Его универсальность и сравнительно низка цена заработали ему популярность среди начинающих пилотов, но пусть вас не обманывает репутация Sidewinder как корабля для новичков. Данная модель — одна из самых маневренных на всём рынке.', colour=0x2F3136)
    emShipsSidewinder.add_field(name='CMDR GIF Community', value='n/a')
    emShipsSidewinder.add_field(name='Dark Enterprise', value='• [DarkWinder](https://s.orbis.zone/4uji)\n• Автор: n/a')
    emShipsSidewinder.set_thumbnail(url='attachment://sidewinder.png')
    emShipsSidewinder.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsSidewinder, delete_after=300)

    # Dark Enterprise
    # DarkWinder - https://s.orbis.zone/4uji /-----/ https://coriolis.io/outfit/sidewinder?code=A2p0u0F0l3d0s3f12j2j0200272725m1m166.Iw1%2FADJQ.Aw1%2BkA%3D%3D.H4sIAAAAAAAAA42QsU4CURREB3fRhV3AXQGJwURlgcTCxNLEgp%2Bw5xMoLCywoaImxMrCT7C09AM0saEjxspQUJNo9F7vkPgSjAWvmEzunDd570ICAN9Zk6%2BRSdj7UI27n6rpXQnQjHRcfm0S3L6rJi9bQDU1SDek6vJLkxKn5blJhfdr9z7Q6O1akyd7v%2BQSSh5CoNyvGDS1ofpy6vKrueVPr9aflTPXPzDJRaKaH8fAId0RXZOuRaeb0l0teXxTPTlfWFMgF66pYILtNuBTEr6vxj%2Ftzzwrya1N5qVJ0iM03LGcUJ1OQ4n%2BiZa3Ijl2%2FTfc%2BbPZ4kEdiOkSLi6l08LaZPEvOXHkxJF0qlg5P%2BCdwyMBAgAA.EweloBjEoUwQwOYBtYhARgtmuJA%3D&bn=DarkWinder


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Sidewinder // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Viper
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Viper // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Viper MkIV
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Viper MkIV // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Vulture
@slash.subcommand(
    base='ships',
    name='vulture',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Vulture»'
)
async def vulture(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/vulture.png', filename='vulture.png')
    # Создаём сообщение
    emShipsVulture = discord.Embed(title='Vulture', description='Создавая Vulture, Core Dynamics выжали всё возможное из своих технологий, оснастив компактный корпус корабля двумя большими гнёздами. Производитель также снабдил Vulture мощными маневровыми двигателями, благодаря которым корабль способен уклоняться от вражеского огня, одновременно нанося значительный урон, что делает Vulture крайне опасным противником.', colour=0x2F3136)
    emShipsVulture.add_field(name='CMDR GIF Community', value='• [2 банки и дробовики](https://s.orbis.zone/cdyg)\n• Автор: <@232550259841171466>')
    emShipsVulture.add_field(name='Dark Enterprise', value='• [Cтервятник для PVE](https://s.orbis.zone/7s3j)\n• [Стервятник на дробашах Хадсона](https://s.orbis.zone/7s3o)\n• Автор: <@270156067055468544>\n\n• [Vulture с пучками](https://s.orbis.zone/22rt)\n• Автор: <@269516916631142411>\n\n• [Вультура с улучшенной плазмой](https://s.orbis.zone/29m0) от Paffoc\n• Автор: Paffoc\n\n• [Стервятник на дробашах](https://s.orbis.zone/7s3q) от Kawaiski\n• Автор: Kawaiski')
    emShipsVulture.set_thumbnail(url='attachment://vulture.png')
    emShipsVulture.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsVulture, delete_after=300)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Vulture // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Challenger
@slash.subcommand(
    base='ships',
    name='challenger',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Alliance Challenger»'
)
async def challenger(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/alliancechallenger.png', filename='alliancechallenger.png')
    # Создаём сообщение
    emShipsChallenger = discord.Embed(title='Alliance Challenger', description='Не что иное, как видоизменённая модель Alliance Chieftain с особым упором на ведение открытого боя. Корабль обладает внушительным количеством гнёзд для орудий, что делает его довольно грозным противником. Хоть Challenger и тяжелее своих «родственников», он тоже отличается характерной для Chieftain маневренностью. При этом корабль оборудован более прочной бронёй, нежели Chieftain, и потому способен дольше продержаться против превосходящих сил противника.', colour=0x2F3136)
    emShipsChallenger.add_field(name='CMDR GIF Community', value='• [PVE с рельсами](https://s.orbis.zone/cdxr)\n• Автор: <@232550259841171466>')
    emShipsChallenger.add_field(name='Dark Enterprise', value='• [PVE challenger](https://s.orbis.zone/3jrw)\n• Автор: <@270156067055468544>\n\n• [Challenger с призмой и улуч. плазмой](https://s.orbis.zone/1sld)\n• Автор: <@235835602317082625>')
    emShipsChallenger.set_thumbnail(url='attachment://alliancechallenger.png')
    emShipsChallenger.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsChallenger, delete_after=300)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Challenger // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Chieftain
@slash.subcommand(
    base='ships',
    name='chieftain',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Alliance Chieftain»'
)
async def chieftain(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/alliancechieftain.png', filename='alliancechieftain.png')
    # Создаём сообщение
    emShipsChieftain = discord.Embed(title='Alliance Chieftain', description='Alliance Chieftain не только представляет угрозу в бою, но и способен избегать огня противника. Lacon Spaceways обеспечили кораблю высокую манёвренность и впечатляющее вооружение, благодаря которому Chieftain может без труда постоять за себя. В трёх внутренних боевых отсеках можно разместить щитонакопитель, а также усилители модулей и корпуса.', colour=0x2F3136)
    emShipsChieftain.add_field(name='CMDR GIF Community', value='• [AX с щитами](https://s.orbis.zone/cdxx)\n• [AX с щитами и ремонтными дронами](https://s.orbis.zone/cdxy)\n• [PVE с плазмой](https://s.orbis.zone/ce3c)\n• Автор: <@232550259841171466>')
    emShipsChieftain.add_field(name='Dark Enterprise', value='• [Chieftain на пиратских лордов](https://s.orbis.zone/4clw)\n• [Chieftain исследователь](https://s.orbis.zone/3y2v)\n• [Chieftain с плазмой и рельсами](https://s.orbis.zone/3y2w)\n• [AX Chieftain](https://s.orbis.zone/3y2u)\n• Автор: <@270156067055468544>')
    emShipsChieftain.set_thumbnail(url='attachment://alliancechieftain.png')
    emShipsChieftain.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsChieftain, delete_after=300)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Chieftain // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Crusader
@slash.subcommand(
    base='ships',
    name='crusader',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Alliance Crusader»'
)
async def crusader(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/alliancecrusader.png', filename='alliancecrusader.png')
    # Создаём сообщение
    emShipsCrusader = discord.Embed(title='Alliance Crusader', description='Представляет собой видоизмененную модель корабля Alliance Chieftain, от которого отличается в первую очередь наличием отсека для истребителя. Crusader имеет три внутренних боевых отсека и место для экипажа из двух человек, что делает его идеально подходящим для практически любого сражения.', colour=0x2F3136)
    emShipsCrusader.add_field(name='CMDR GIF Community', value='n/a')
    emShipsCrusader.add_field(name='Dark Enterprise', value='• [PvE Crusader](https://s.orbis.zone/3jro)\n• [Crusader на дробашах](https://s.orbis.zone/3jrs)\n• Автор: <@270156067055468544>')
    emShipsCrusader.set_thumbnail(url='attachment://alliancecrusader.png')
    emShipsCrusader.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsCrusader, delete_after=300)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Crusader // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Asp Explorer
@slash.subcommand(
    base='ships',
    name='aspe',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Asp Explorer»'
)
async def aspe(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/aspexplorer.png', filename='aspexplorer.png')
    # Создаём сообщение
    emShipsAspe = discord.Embed(title='Asp Explorer', description='Часто продаётся в качестве идеального корабля для пилотов, подбирающих свой первый корабль для нескольких экипажей (Multi-Crew). Его большая дальность прыжка и широкий фонарь кабины с хорошим обзором заработали этому творению Lakon Spaceways популярность среди исследователей, но универсальность данной модели также делает его отличным вариантом для торговцев и боевых пилотов. Для Asp Explorer подходят посадочные площадки среднего размера.', colour=0x2F3136)
    emShipsAspe.add_field(name='CMDR GIF Community', value='• [ASP для начинающих](https://s.orbis.zone/cl82)\n• Автор: <@360125693729964043>')
    emShipsAspe.add_field(name='Dark Enterprise', value='• [ASP Исследователь](https://s.orbis.zone/3oi8)\n• [Боевой АСП](https://s.orbis.zone/3oi9)\n• [ASP Майнер 3.3](https://s.orbis.zone/3oia)\n• [ASP Майнер пейнита](https://s.orbis.zone/3utw)\n• Автор: <@270156067055468544>')
    emShipsAspe.set_thumbnail(url='attachment://aspexplorer.png')
    emShipsAspe.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsAspe, delete_after=300)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Asp Explorer // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Asp Scout
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Asp Scout // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Assault Ship
@slash.subcommand(
    base='ships',
    name='fas',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Federal Assault Ship»'
)
async def fas(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/federalassaultship.png', filename='federalassaultship.png')
    # Создаём сообщение
    emShipsFAS = discord.Embed(title='Federal Assault Ship', description='Многие из клиентов Core Dynamics считали, что их десантные корабли должны выполнять более определённые задачи. Ответом на эти запросы стал атакующий корабль. Он лучше приспособлен для боевых действий, чем исходный вариант. У него выше маневренность, а вооружение мощнее у расположено удачнее. Ради этих модификаций пришлось пожертвовать вместительностью, вследствие чего он менее универсален, но лучше справляется со своей специализированной ролью.', colour=0x2F3136)
    emShipsFAS.add_field(name='CMDR GIF Community', value='• [PVE с рельсами](https://s.orbis.zone/cdxu)\n• [AX с щитами и дронами](https://s.orbis.zone/cdye)\n• Автор: <@232550259841171466>')
    emShipsFAS.add_field(name='Dark Enterprise', value='• [Бронированный FAS с торпедами](https://s.orbis.zone/2_we)\n• Автор: <@189334900405436416>\n\n• [FAS 355](https://s.orbis.zone/3jti)\n• [FAS Explorer](https://s.orbis.zone/adp)\n• [FAS AX](https://s.orbis.zone/42ww)\n• [PVE FAS](https://s.orbis.zone/3jtp)\n• [ФАС с мультиками и плазмой](https://s.orbis.zone/3jts)\n• Автор: <@270156067055468544>')
    emShipsFAS.set_thumbnail(url='attachment://federalassaultship.png')
    emShipsFAS.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsFAS, delete_after=300)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Assault Ship // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Dropship
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Dropship // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Gunship
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Gunship // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Fer-de-Lance
@slash.subcommand(
    base='ships',
    name='fdl',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Fer-de-Lance»'
)
async def fdl(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/ferdelance.png', filename='ferdelance.png')
    # Создаём сообщение
    emShipsFDL = discord.Embed(title='Federal Assault Ship', description='Fer-de-Lance — это тяжёлый боевой корабль производства Zorgon Peterson. За четыре средних и одно гигантское гнездо на борту корабль можно смело назвать серьезным противником, справиться с которым будет нелегко даже Anaconda и Federal Corvette. Если у него и есть недостатков, то это его узкая специализация. Покупателям не рекомендуется использовать Fer-de-Lance для какой-то другой деятельности, кроме боя.', colour=0x2F3136)
    emShipsFDL.add_field(name='CMDR GIF Community', value='n/a')
    emShipsFDL.add_field(name='Dark Enterprise', value='• [PvP Fer-Lance-De](https://s.orbis.zone/6vso)\n• [PvP Conduit Plasma](https://s.orbis.zone/6zyu)\n• [PvP Реверсный](https://s.orbis.zone/7s9w)\n• [FDL Explorer](https://s.orbis.zone/6vsg)\n• [FDL с многостволками](https://s.orbis.zone/6vsz)\n• Автор: <@270156067055468544>\n\n• [PvP FDL с двухпоточником](https://s.orbis.zone/2-k0)\n• [AX FDL](https://s.orbis.zone/20u8)\n• Автор: Equalizer\n\n• [AX FDL v2](https://s.orbis.zone/5x7m)\n• Автор:  <@305091226611351572>')
    emShipsFDL.set_thumbnail(url='attachment://ferdelance.png')
    emShipsFDL.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsFDL, delete_after=300)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Fer-de-Lance // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Keelback
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Keelback // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait MkII
@slash.subcommand(
    base='ships',
    name='krait',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Krait MkII»'
)
async def krait(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/kraitmk2.png', filename='kraitmk2.png')
    # Создаём сообщение
    emShipsKrait = discord.Embed(title='Krait MkII', description='Переделка Krait Lightspeeder, который изначально производили Faulcon DeLacy в 3100-х. И хотя новинка крупнее оригинала, у них сходные характеристики, скорость, манёвренность, а огневая мощь превышает уровень защиты. Также в корабле присутствует отсек для истребителя и место для экипажа из двух человек, благодаря чему он представляет собой хороший вариант для тех, кому требуется многофункциональный корабль среднего веса.', colour=0x2F3136)
    emShipsKrait.add_field(name='CMDR GIF Community', value='n/a')
    emShipsKrait.add_field(name='Dark Enterprise', value='• [Исследовательский Krait](https://s.orbis.zone/3qky)\n• [PVE Krait](https://s.orbis.zone/4z1s)\n• [Krait с плазмой](https://s.orbis.zone/3uxf)\n• [Krait на дробашах](https://s.orbis.zone/3uxi)\n• [Krait AX](https://s.orbis.zone/3980)\n• [Krait майнер 3.3](https://s.orbis.zone/3uxn)\n• [Майнер пейнита](https://s.orbis.zone/3uxs)\n• [PvP Krait v2](https://s.orbis.zone/4c1d)\n• Автор: <@270156067055468544>')
    emShipsKrait.set_thumbnail(url='attachment://kraitmk2.png')
    emShipsKrait.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsKrait, delete_after=300)
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait MkII // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait Phantom
@slash.subcommand(
    base='ships',
    name='phantom',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Krait Phantom»'
)
async def phantom(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/kraitphantom.png', filename='kraitphantom.png')
    # Создаём сообщение
    emShipsPhantom = discord.Embed(title='Krait Phantom', description='Krait Phantom считается универсальным судном для любого пилота благодаря вместительному грузовому отсеку и довольно-таки внушительному арсеналу гнёзд. Ему хватит огневой мощи, чтобы сдержать натиск более крупных целей, а по своей скорости он может соревноваться с кораблями заметно меньше собственного размера — во всяком случае, при полёте по прямой. Ещё одно достоинство модели — восемь внутренних отделений, которые пилот может обустроить по своим потребностям. Корабль куда быстрее и легче своего собрата, Krait Mk II, хоть и уступает ему по вооружению.', colour=0x2F3136)
    emShipsPhantom.add_field(name='CMDR GIF Community', value='• [Pathfinder](https://s.orbis.zone/cc4g)\n• Автор: <@232550259841171466>')
    emShipsPhantom.add_field(name='Dark Enterprise', value='• [Phantom исследователь](https://s.orbis.zone/48_o)\n• [PVE Phantom](https://s.orbis.zone/42yo)\n• [AX Phantom](https://s.orbis.zone/42wx)\n• [PvP Phantom Prisma](https://s.orbis.zone/47tu)\n• [PvP Phantom Bi-We](https://s.orbis.zone/7s98)\n• Автор: <@270156067055468544>\n\n• [Бронированный исследовательский фантом](https://s.orbis.zone/46rl)\n• Автор: Andrew An')
    emShipsPhantom.set_thumbnail(url='attachment://kraitphantom.png')
    emShipsPhantom.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsPhantom, delete_after=300)
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait Phantom // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait Phantom
@slash.subcommand(
    base='ships',
    name='mamba',
    base_desc='Сборки по кораблям',
    description='Список сборок для «Mamba»'
)
async def mamba(ctx):
    # Загружаем картинку корабля
    file = discord.File('sources/images/mamba.png', filename='mamba.png')
    # Создаём сообщение
    emShipsMamba = discord.Embed(title='Mamba', url='https://elite-dangerous.fandom.com/ru/wiki/Mamba', description='В основу разработки Mamba был положен прототип гоночного корабля, так и не увидевшего свет, поэтому нет ничего удивительного в том, что эта модель является одной из самых быстрых из находящихся в производстве. При этом одно гнездо четвертого класса и два — третьего обеспечивают ему достойную огневую мощь. В сочетании со скоростью это позволяет пилоту нанести молниеносный удар и исчезнуть до того, как цель откроет ответный огонь. Безусловно, судно во многом напоминает Fer-de-Lance — другой корабль производства Zorgon Peterson, — однако Mamba легко обгонит его при полёте по прямой, пусть и не обладает такой же манёвренностью.', colour=0x2F3136)
    emShipsMamba.add_field(name='CMDR GIF Community', value='n/a')
    emShipsMamba.add_field(name='Dark Enterprise', value='• [PVE Mamba](https://s.orbis.zone/6v9z)\n• [PVP JellyFish](https://s.orbis.zone/6v9x)\n• [PvP Multi-Cannon](https://s.orbis.zone/6v9s)\n• Автор: <@270156067055468544>\n\n• [PvP Duel Multi-Cannon](https://s.orbis.zone/7s05) \n• Автор: AndrewAn')
    emShipsMamba.set_thumbnail(url='attachment://mamba.png')
    emShipsMamba.set_footer(text=client.user.name + ' // Полный список кораблей /allships')
    # Отправляем сообщение и удаляем его через 300 секунд (5 минут)
    await ctx.send(file=file, embed=emShipsMamba, delete_after=300)
# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait Phantom // КОНЕЦ


# Генерируемый токен при создание приложения на странице https://discord.com/developers/applications, необходимый для подключения к серверу
# Прописывается в config.py
client.run(config.token)

# ------------- СОЗДАЁМ ПРИЛОЖЕНИЕ И НАЗЫВАЕМ ЕГО CLIENT  // КОНЕЦ