# -*- coding: utf-8 -*-

# region •••••••••••••••• ИМПОРТ МОДУЛЕЙ
import discord  # Импортируем библиотеку работы с Discord API (Application Programming Interface)
from discord.commands import permissions  # Импортируем библиотеку разрешений для комманд
from discord.commands import SlashCommandGroup
import logging  # Импортируем библиотеку журналирования
import config   # Импортируем настройки приложения


# endregion ••••••••••••• ИМПОРТ МОДУЛЕЙ // КОНЕЦ


# •••••• 😈 •••••• СОЗДАЁМ ПРИЛОЖЕНИЕ И НАЗЫВАЕМ ЕГО CLIENT
client = discord.Bot(description=config.app_short_description)

# region •••••••••••••••• СОЗДАЁМ ШАБЛОН ДЛЯ GUILDS ID В КОМАНДАХ С КОСОЙ ЧЕРТОЙ
def guild_ids_for_slash():
    """
    В зависимости от установленной переменной "test" или "prod" шаблон подставляет нужное значение в "guild_ids"
    """
    if config.environment_type == 'prod':
        return None
    else:
        return [guild.id for guild in client.guilds]


# endregion ••••••••••••• СОЗДАЁМ ШАБЛОН ДЛЯ GUILDS ID В КОМАНДАХ С КОСОЙ ЧЕРТОЙ // КОНЕЦ


# region •••••••••••••••• СОЗДАЁМ ШАБЛОН С ССЫЛКОЙ ДЛЯ ПОДКЛЮЧЕНИЯ К СЕРВЕРУ
def get_invite_link(bot_id):
    return f'https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot%20applications.commands'


# endregion ••••••••••••• СОЗДАЁМ ШАБЛОН С ССЫЛКОЙ ДЛЯ ПОДКЛЮЧЕНИЯ К СЕРВЕРУ


# region •••••••••••••••• ВЫВОДИМ ДАННЫЕ ПРИЛОЖЕНИЯ ПРИ ПОДКЛЮЧЕНИЕ В КОНСОЛЬ
@client.event
async def on_ready():
    # Console Log // Выводим данные приложения в консоль Python
    logger.info(f'APP Username: {client.user} ')
    logger.info(f'Using token {config.token[0:2]}...{config.token[-3:-1]}')
    logger.info(f'Current env type: {config.environment_type}')
    logger.info('APP Client ID: {0.user.id} '.format(client))

    # Console Log // Выводим ссылку для подключения приложения к серверу в консоль Python
    logger.info(f'Link for connection: {get_invite_link(client.user.id)}')

    # Console Log // Выводим список серверов к которым подключено приложение в консоль Python
    logger.info('Servers connected to: ' + ''.join('"' + guild.name + '"; ' for guild in client.guilds))

    # Изменяем статус приложения
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Elite Dangerous'))


# endregion ••••••••••••• ВЫВОДИМ ДАННЫЕ ПРИЛОЖЕНИЯ ПРИ ПОДКЛЮЧЕНИЕ В КОНСОЛЬ // КОНЕЦ


# region •••••••••••••••• РЕГИСТРИРУЕМ СОБЫТИЯ ПРИЛОЖЕНИЯ В КОНСОЛЬ
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(process)d:%(thread)d: %(module)s:%(lineno)d: %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# endregion ••••••••••••• РЕГИСТРИРУЕМ СОБЫТИЯ ПРИЛОЖЕНИЯ В КОНСОЛЬ // КОНЕЦ


# region •••••••••••••••• КОМАНДА ПРОВЕРКА ПРИЛОЖЕНИЯ
@client.slash_command(guild_ids=guild_ids_for_slash(), default_permission=False, name='ping', description='Проверить состояние приложения')
@permissions.is_owner()
async def ping(ctx):
    # Создаём сообщение
    embed = discord.Embed(title='ВНИМАНИЕ!', description=f'Задержка {round(client.latency * 100, 1)} ms', colour=0x90D400)
    # Отправляем скрытое сообщение
    await ctx.respond(embed=embed, ephemeral=True)

# endregion ••••••••••••• КОМАНДА ПРОВЕРКА ПРИЛОЖЕНИЯ // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ ИНФОРМАЦИИ О ПРИЛОЖЕНИИ
@client.slash_command(guild_ids=guild_ids_for_slash(), default_permission=True, name='information', description='Показать информацию о приложение')
async def information(ctx):
    # Создаём сообщение
    embed = discord.Embed(title='ИНФОРМАЦИЯ', description=f'```{config.app_full_description}```', colour=0x2F3136)
    embed.set_thumbnail(url=f'{client.user.avatar.url}')
    embed.set_footer(icon_url=f'{ctx.author.avatar.url}', text=f'Информация запрошена: {ctx.author.name}')
    invite_app = discord.utils.oauth_url(client_id=client.user.id, permissions=discord.Permissions(),scopes=("bot", "applications.commands"))
    # Создаём кнопки
    button = discord.ui.View()
    button.add_item(discord.ui.Button(label='Сервер поддержки', url=config.app_support_server_invite, style=discord.ButtonStyle.url))
    button.add_item(discord.ui.Button(label='Добавить на сервер', url=invite_app, style=discord.ButtonStyle.url))
    button.add_item(discord.ui.Button(label='GitHub', url=config.app_github_url, style=discord.ButtonStyle.url))
    # Отправляем сообщение и удаляем его через 60 секунд
    await ctx.respond(embed=embed, view=button, delete_after=60)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ ИФОРМАЦИИ О ПРИЛОЖЕНИЕ // КОНЕЦ


# region •••••••••••••••• КОМАНДА ВЫВОДА СПИСКА СЕРВЕРОВ
@client.slash_command(guild_ids=guild_ids_for_slash(), default_permission=False, name='servers', description='Вывести список серверов, к которым подключено приложение')
@permissions.is_owner()
async def servers(ctx):
    # Создаём сообщение
    embed = discord.Embed(title='СПИСОК СЕРВЕРОВ', description='```Список серверов, к которым подключено приложение.```', colour=0x2F3136)
    embed.add_field(name='СПИСОК СЕРВЕРОВ:', value=''.join(guild.name + f' (ID:{guild.id})\n' for guild in client.guilds))
    # Отправляем скрытое сообщение
    await ctx.respond(embed=embed, ephemeral=True)


# endregion ••••••••••••• КОМАНДА ВЫВОДА СПИСКА СЕРВЕРОВ // КОНЕЦ


# region •••••••••••••••• СОЗДАЁМ ГРУППУ SHIPS ДЛЯ КОМАНД С КОСОЙ ЧЕРТОЙ
ships = SlashCommandGroup("ships", "Команды связанные с короблями.")
client.add_application_command(ships)


# endregion ••••••••••••• СОЗДАЁМ ГРУППУ SHIPS ДЛЯ КОМАНД С КОСОЙ ЧЕРТОЙ // КОНЕЦ


# endregion ••••••••••••• TODO: Предпологаемое меню
class menu_ships(discord.ui.View):
    @discord.ui.select(placeholder='Выберите корабль, чтобы показать список сборок', min_values=1, max_values=1, options=[
        #discord.SelectOption(label='Adder', description='Небольшой корабль', emoji='❌'),
        #discord.SelectOption(label='Cobra MkIII', description='Небольшой корабль'),
        #discord.SelectOption(label='Cobra MkIV', description='Небольшой корабль', emoji='❌'),
        #discord.SelectOption(label='Diamondback Explorer', description='Небольшой корабль'),
        #discord.SelectOption(label='Diamondback Scout', description='Небольшой корабль', emoji='❌'),
        #discord.SelectOption(label='Dolphin', description='Небольшой корабль'),
        #discord.SelectOption(label='Hauler', description='Небольшой корабль', emoji='❌'),
        #discord.SelectOption(label='Imperial Courier', description='Небольшой корабль'),
        #discord.SelectOption(label='Imperial Eagle', description='Небольшой корабль', emoji='❌'),
        discord.SelectOption(label='Sidewinder', description='Небольшой корабль'),
        #discord.SelectOption(label='Viper', description='Небольшой корабль', emoji='❌'),
        #discord.SelectOption(label='Viper MkIV', description='Небольшой корабль', emoji='❌'),
        #discord.SelectOption(label='Vulture', description='Небольшой корабль'),
    ])
    async def select_callback(self, select, interaction):
        await interaction.response.send_message(f'Это меню находится в разработке', ephemeral=True)


# endregion


# region •••••••••••••••• СОЗДАЁМ ШАБЛОН СООБЩЕНИЯ SHIPS LIST
embed_ships_list = discord.Embed(
        title="СПИСОК КОМАНД ПО КОРАБЛЯМ",
        description="```Список всех сборок кораблей которые на данный момент доступны в приложение.```",
        colour=0x2F3136)
embed_ships_list.add_field(
        name="Небольшие корабли",
        value="• Adder `❌`\n"
              "• Cobra MkIII `/ships cobramk3`\n"
              "• Cobra MkIV `❌`\n"
              "• Diamondback Explorer `/ships dbe`\n"
              "• Diamondback Scout `❌`\n"
              "• Dolphin `/ships dolphin`\n"
              "• Eagle `❌`\n"
              "• Hauler `❌`\n"
              "• Imperial Courier `/ships courier`\n"
              "• Imperial Eagle `❌`\n"
              "• Sidewinder `/ships sidewinder`\n"
              "• Viper `❌`\n"
              "• Viper MkIV `❌`\n"
              "• Vulture `/ships vulture`")
embed_ships_list.add_field(
        name="Средние корабли",
        value="• Alliance Challenger `/ships challenger`\n"
              "• Alliance Chieftain `/ships chieftain`\n"
              "• Alliance Crusader `/ships crusader`\n"
              "• Asp Explorer `/ships aspe`\n"
              "• Asp Scout `❌`\n"
              "• Federal Assault Ship `/ships fas`\n"
              "• Federal Dropship `❌`\n"
              "• Federal Gunship `❌`\n"
              "• Fer-de-Lance `/ships fdl`\n"
              "• Keelback `❌`\n"
              "• Krait MkII `/ships krait`\n"
              "• Krait Phantom `/ships phantom`\n"
              "• Mamba `/ships mamba`\n"
              "• Python `/ships python`\n"
              "• Type-6 Transporter `/ships type6`")
embed_ships_list.add_field(
        name="Крупные корабли",
        value="• Anaconda `/ships anaconda`\n"
              "• Beluga Liner `❌`\n"
              "• Federal Corvette `/ships corvette`\n"
              "• Imperial Clipper `❌`\n"
              "• Imperial Cutter `/ships cutter`\n"
              "• Orca `❌`\n"
              "• Type-7 Transporter `/ships type7`\n"
              "• Type-9 Heavy `/ships type9`\n"
              "• Type-10 Defender `/ships type10`",
        inline=False)
embed_ships_list.add_field(
        name="Дополнительно",
        value="• [Таблица для сравнения дальности прыжка всех иследовательских кораблей](https://docs.google.com/spreadsheets/d/15iW5-Gnni7PELS5DSoVM4prIqEA9Cnz8do8w7nIbvCU/)",
        inline=True)


# endregion ••••••••••••• СОЗДАЁМ ШАБЛОН СООБЩЕНИЯ SHIPS LIST // КОНЕЦ


# region •••••••••••••••• СОЗДАЁМ ГРУППУ КНОПОК ДЛЯ СПИСКИ КОРАБЛЕЙ
class Button_group_for_ships(discord.ui.View):
    @discord.ui.button(
        label='СПИСОК КОРАБЛЕЙ',
        custom_id="button_ships_list",
        style=discord.ButtonStyle.primary,
        emoji='🗒️'
    )
    async def button_callback(self, button, interaction):
        await interaction.response.send_message(embed=embed_ships_list, view=menu_ships(), ephemeral=True)


# endregion ••••••••••••• СОЗДАЁМ ГРУППУ КНОПОК ДЛЯ СПИСКИ КОРАБЛЕЙ // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СООБЩЕНИЯ SHIPS LIST + ННОПКИ SHIPS LIST
@ships.command(default_permission=False, name="list", description="Список команд для вызова сборок по кораблям.")
async def ships_show(ctx):
    await ctx.respond(embed=embed_ships_list, view=menu_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СООБЩЕНИЯ SHIPS LIST + ННОПКИ SHIPS LIST // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Cobra Mk III
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="cobramk3", description="Список сборок для «Cobra Mk III»")
async def cobramk3(ctx):
    file = discord.File("sources\images\corporations\delacy-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Cobra Mk III",
        description="```Настоящий многофункциональный корабль. Cobra Mk III отлично подходит для целевого спектра задач. В бою он способен нанести ощутимый урон и при необходимости может быстро покинуть сражение, а его просторный трюм позволяет перевозить большой объём грузов, чем другие корабли сходного размера и ценовой категории. Cobra также отлично подходит для исследователей благодаря своему вместительному топливному баку и шести внутренним отделениям.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value="• [Cobra MK III Универсальная](https://s.orbis.zone/7sa9)\n"  # https://coriolis.io/outfit/cobra_mk_iii?code=A2pataFalddasaf427270p0p04043245030101v6002i.Iw1%2FgDJQ.Aw18cQ%3D%3D.H4sIAAAAAAAAA42Rr0sEURSFz87ujDu%2FHGfdWQcFQXfUZjNsEZsWQbBsEcxi2CBYNmgzGEQEwWQwGoyGjf4BRoOI0aAmk67veu7CPow74ePw7jf3ce%2BDGQPw6xL9cyLsOUB8FAFpm6l2HwLFVwmQklm1Zpeobv2IJK%2FLQOOuQvORjcQxDSsdEEnxLVJ%2FJ7LrBMjVbHamaJbNtDUPh%2Bbguno3o%2FnMirimZaVjwo%2BMSHCRAnOa5jUtaFrUJFXTtjonQEV7uu0ZwLuNefGgpz%2BKFJhtK80S7q7P%2Bv6nSL72IdI8exORcBQpMutWutIF33gcVneXasof%2BE%2BhSWKzYc1LNTscLFUUpwHridm09T3Cyfsinm40bJX5Xi9E9jTOdj19iszsDPXaxBKwcjLJU8H%2F7w%2Fx1ksa%2FgEAAA%3D%3D.EweloBhBGA2EAcICmBDA5gG2SGF8hRFA&bn=Cobra%20Universal
              "• Автор: <@461538602715971594>\n\n"
              
              # Автор HarrisonSould
              "• [Кобра без орудий для путешествий](https://s.orbis.zone/1slr)\n"  # https://coriolis.io/outfit/cobra_mk_iii?code=A0pdtdFaldddsdf4----02-33450301v62i.Iw1%2FkA%3D%3D.Aw1%2FkA%3D%3D..EweloBhBGA2MoFMCGBzANokMK5FAoA%3D%3D&bn=Cobra%20PVE
              "• Автор: <@270156067055468544>\n\n"
              
              # Автор Andrew An
              "• [Кобра исследователь](https://s.orbis.zone/2tf3)\n"  # https://coriolis.io/outfit/cobra_mk_iii?code=A0p8tdFaldd3sdf4------321P480d2iv6.Iw18gDCQ.Aw1%2FkA%3D%3D.H4sIAAAAAAAAA1WPOw4BURiFj%2Fc7wxiP6Lw7odCIxAYsQCOxBBoUEgqF2gqUSqVCoVBagogFKBSiEP7ff8XcxBRfJjnfPfdckA%2FA2yN4LQWhnROIzMJArCN%2F5jYEFO4OgB3U0uZU4D8EAKP5YE6uDMmdlNT5UGAUnszWVZBQeXrjBvL9lJguymhzZJvfm6xJQsyTJOymmi0Z46vkxzMze6ihj84FAVUYrMaArCrJKRQVSmES3Uu9%2F5L9hbmiNnOU2rppgN9LTCVZ67dsViPSvZuYJnVt04yWgfoiLvsY9vcBK1p89EMBAAA%3D.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=Cobra%20explorer
              "• Автор: Andrew An\n\n"
              
              # Автор Klemyr
              "• [Быстрая Кобра (Boost 608 m/s)](https://s.orbis.zone/2_xu)\n"  # https://coriolis.io/outfit/cobra_mk_iii?code=A4pataFaladasaf427270p0p0404322bB3v6m3m32525.Iw1%2FgDJQ.IzAM4yLUXI%3D%3D.H4sIAAAAAAAAA42RO0sDQRSFbx67JNkkmyx5%2BUDUrBaidhaCaCmIiGBhQAvtRBsLiyDaWdiJjYWVgqWFpaWFf8FKC2sfCBKCaDLHc4Vd0SpbHM7O%2FeaemTtibBFpW5TWEcW7fwIyaQPkl%2BMifldCxDmnQ8TMKBlRcp%2FiKlS6YinR4CKiphR22tG6%2FwlUtF7o%2BwKKx65IdbtMMma6Q7KumddOgD9wsbBXJGSZyQAa0qThlZxIUl1K3YC6QXWwzVpAejePgFt%2FAcanmgASphYmxShWrUfEvszwJJoUX2Umkp1AKbMUQJWDBmDt0tobH0D18BkoZ3UEzi%2Fkzbd5nQklX6Mk595Jrr%2BR3OIv0mY2zDzVYS1yRJXbpEj%2Bgg%2FiqzgqyHRMumYsJE8o2SZnnx9tAf40L%2BOoQ84shNCmtjvjs%2FBEJLWx%2F%2FNABTPyp5NzR5vt7yWkztM9vjoUOyYh%2F75vsJ9Vm3oCAAA%3D.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=Valor%20(Fast%20PVE)
              "• Автор: <@189334900405436416>")
    embed.set_image(url='attachment://delacy-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Cobra Mk III // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Cobra MkIV
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Cobra MkIV // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Diamondback Explorer
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="dbe", description="Список сборок для «Diamondback Explorer»")
async def dbe(ctx):
    file = discord.File("sources\images\corporations\lakon-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Diamondback Explorer",
        description="```Более крупный собрат Diamondback Scout, также представляет собой корабль двойного назначения, ориентированный на бои и исследования. Выдающаяся огневая мощь и система гнёзд Explorer делают более универсальным по сравнению со Scout, а большая дальность прыжка и превосходная теплоэффективность отлично подойдут исследователям.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value="• [DBE за 77](https://s.orbis.zone/czgy)\n"  # https://coriolis.io/outfit/diamondback_explorer?code=A0p0tdFfldd3sdf4-------321P0i43v61y9q2i.Iw18SQ%3D%3D.Aw18SQ%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8Zw9XWQ8kOI5wMjDw23z7%2F19sAT9QnumfGFy%2BDEjwq%2Fz6%2F19E7vf%2F%2F6IgeYkNLAwMygXiQJXM%2F6TgKitgKsE2iURIA1XeAcr8Z%2FlnCFPEX%2FEGKH%2Fm3v%2F%2F%2F1n%2FWcG1tgAJTpCBXAaCDAyKIEOUQIQqiFDj%2BQdUzvYvAdWQAw%2F%2B%2F9cDufm%2F0D8fuEmFDFCfCIEUiaz4C3QzyBESCR%2BAKsX%2BxcJUCgmoMzCYdggD3fefAQYATsmgtEMBAAA%3D.EwegLCAMUgjAbCUBTAhgcwDbJHS%2BZpIg
              "• Автор: <@184299323624783872>\n\n"
              
              # Автор Klemyr
              "• [DBE Explorer](https://s.orbis.zone/qov)\n"  # https://coriolis.io/outfit/diamondback_explorer?code=A0p0tdFfldd3sdf4-------1P3243v62i2f.Iw1%2FADGQ.Aw18UA%3D%3D.H4sIAAAAAAAAAz2OvQ7BYBSGT6sVf0m1isYi%2FjdhFQmjwT1wCSzSgXtwGUaDwehCDGI2GBqD6DnOm6hvePPlPM%2BbcwyeEFFsaHx2GplIv06BRSpHi0hMDsBN8I2Gs1LkI8q%2BTRTsVW%2FNIhFJcQ2mDTOE2X6LeOc8kb8tq3lVIhYPIVngy6fy012rNo%2BSanZVJcoNXKIG%2Bk1EB9HFTZLmZWI64UP7l5tIf%2FxS5PL8v38NjqkHyT%2FEei72B9gpJV4kplfsEQ2ndT1N6Pe%2Br5CN6xMBAAA%3D.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=DBE%20Explorer
              "• Автор: <@189334900405436416>\n\n"
              
              "• [DBE Explorer 71.80 прыжок](https://s.orbis.zone/2wux)\n"  # https://coriolis.io/outfit/diamondback_explorer?code=A0p0tdFfldd3sdf4---02---1P32430i0Vv69q2i.Iw1%2BgDC1A%3D%3D%3D.Aw18SQ%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8ZwdXWQ8kOAJ%2B%2F%2F%2FP%2F0CPgUFsAwtQ5QWgQf%2BZ%2FonBFZUBCX6VX%2F%2F%2Fi7wBEqIL%2BBkYJEAqlQvEgSqZ%2F0nBVVbAVIKtE6kRBaq8A5T5z%2FLPEKSIBSSf8AEov%2BXR%2F%2F%2F%2FWf9ZwbU2AAlOkIFcBoIMDIogQ5RAhCqIUOP5B1TO9i8Bppy%2F4g3QkAMP%2Fv%2FXs%2FkGlOL%2Bp4YqdeYeUFTwnw%2Fc%2FByQFEitEEheZMVfoE9ATpMAOee%2F2L9YmEohAXUGBtMOYaCr%2FzPAAQDt0L78XwEAAA%3D%3D.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=DBE%20Jumpy
              "• Автор: <@269516916631142411>")
    embed.set_image(url='attachment://lakon-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Diamondback Explorer // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Diamondback Scout
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Diamondback Scout // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Dolphin
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="dolphin", description="Список сборок для «Dolphin»")
async def dolphin(ctx):
    file = discord.File("sources\images\corporations\saud-kruger-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Dolphin",
        description="```Как и у других пассажирских судов Saud Kruger, на борту Dolphin можно установить каюту класса люкс и создать комфортабельные условия для перевозки пассажиров. И несмотря на значительно меньшую стоимость, чем у его собратьев, Beluga Liner и Orca, Dolphin обладает такой же плавностью линий корпуса и изысканностью.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value="• [Планетарные операции](https://s.orbis.zone/h4ns)\n"  # https://coriolis.io/outfit/dolphin?code=A0patfFaliddsdf42d2d02--1O320W431E1Ev62i3w.AwRj4yqA.IwBj48CYIZmKQ%3D%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf85wBXWQMkOOY8%2B%2F9f6AJQu5jKr%2F%2F%2F%2FzP9E4PLlwAJfpCoiNzv%2F%2F9FF%2FAzMEhsYGFgUC4QB5rE%2FE8KrrICphJsk0iNKFDlHaDMf5Z%2FhjBF%2FBVvgPJn7gEtYf1nBdfaCCQ4QQZyGQgyMCiCDFECEaogQo3nH1A5279EmHIhAXUGBj2PL%2F%2F%2FS%2FrIAs3n%2BBcGN6kLSLCFfPr%2Fn3%2FCC6BNN%2B78%2Fy%2BR8AGon5MYRVz%2FOLG4VOCfD1xrLkjK5htQCiQvsuIvMExAnoToF%2FkXi%2BJI0w5hoPv%2BMyABAJBkKYOmAQAA.IwegLCoAyQbHICmBDA5gG0SSVchgUA%3D%3D&bn=Fake%20Taxi
              "• Автор: <@232550259841171466>")
    embed.set_image(url='attachment://saud-kruger-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Dolphin // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Hauler
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Hauler // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Courier
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="courier", description="Список сборок для «Imperial Courier»")
async def courier(ctx):
    file = discord.File("sources\images\corporations\gutamaya-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Imperial Courier",
        description="```Одно из самых компанктных судов на рынке, Imperial Courier представляет собой лёгкий боевой корабль от Gutamaya. Он может похвастаться маневренностью, которая составит конкуренцию даже Viper MkIII, и способен с лёгкостью уходить от огня противника, в то время как три средних гнезда сделали его популярным среди пилотов, ищущих хорошее сочетание силы и стиля.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор Artificial Intelligence
              "• [Скоростной для планетарных операций(FSD 4A v1)](https://s.orbis.zone/h5ur)\n"  # https://coriolis.io/outfit/imperial_courier?code=A0p0tzF5l3dds8f3--2d02---2t1N3uv6011y2i3w.AwRj4ypI.IwBj4iCYwZnKQ%3D%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8ZwdXWQskOAJ%2B%2F%2F%2FP%2F0CPgUFsAwtQ5QWgQf%2BZ%2FonBFRUDCX6VX%2F%2F%2Fi8gBVYou4GdgkACpVC4QB6pk%2FicFV1kBUwm2TiRCGqjyDlDmP8s%2FQ5gi%2Foo3QPkz9%2F7%2F%2F8%2F6zwqutRFIcIIM5DIQZGBQBBmiBCJUQYQazz%2BgcrZ%2FCaiGHHjw%2F7%2BezTegFNe%2FMLhJfUCCLeQT0E8TXgAV3bjz%2F79EwgegIu5%2FnFgcIfjPD641ByQF8p8gKExUwP4T%2FRcLkxcSUGdgMAUR%2F%2F8zIAAACkubBHsBAAA%3D.IwegLCoAwgHOICmBDA5gG0SSVchgUA%3D%3D&bn=Superbolide
              "• [Скоростной для планетарных операций(FSD 4A)](https://s.orbis.zone/h5us)\n"  # https://coriolis.io/outfit/imperial_courier?code=A0p0tzF5l3dds8f3--2d02---2t1N3uv6011y2i3w.AwRj4ypI.IwBj4iCYwZnKQ%3D%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8ZwdXWQskOAJ%2B%2F%2F%2FP%2F0CPgUFsAwtQ5QWgQf%2BZ%2FonBFRUDCX6VX%2F%2F%2Fi8gBVYou4GdgkACpVC4QB6pk%2FicFV1kBUwm2TqRGFKjyDlDmP8s%2FQ5gi%2Foo3QPkz9%2F7%2F%2F8%2F6zwqutRFIcIIM5DIQZGBQBBmiBCJUQYQazz%2BgcrZ%2FCaiGHHjw%2F7%2BezTegFNe%2FMLhJfUCCLeQT0E8TXgAV3bjz%2F79EwgegIu5%2FnFgcIfjPD641ByQF8p8gKExUwP4T%2FRcLkxcSUGdgMAUR%2F%2F8zIAAAs8GXVHsBAAA%3D.IwegLCoAwgHOICmBDA5gG0SSVchgUA%3D%3D&bn=Superbolide
              "• Авторы: <@232550259841171466>\n\n"
              
              # Автор HarrisonSould
              "• [Быстрый курьер](https://s.orbis.zone/3z6y)\n"  # https://coriolis.io/outfit/imperial_courier?code=A0p8tzF5l3dds8f2---02---2t1N3uv6242i3w-.Iw18QDJQ.Aw18SQ%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8Zw9XWQ8kOI5wMjDw23z7%2F19sAT9QnumfGFy%2BBEjwq%2Fz6%2F1%2FkDZAQBclLbGBhYFAuEAeqZP4nBVdZDlMJtkmkRhSo8g5Q5j%2FLP0OYIv6KN0D5M%2Ff%2B%2F%2F%2FP%2Bs8SrrUFSHDy%2FPv%2Fn2uKIAODIoilBGKpglhqINZ%2Ftn8JqIYcePD%2Fvx7Izf%2B5%2F6mBpBhBUhJ%2FgFI574Cigv984OYXMkD9JwTSKrLiL9AnIKdJJHwAqhT5FwtSCfQUg5CDPAODKTgQ%2FjPAAQAtuxh%2BWgEAAA%3D%3D.EwegLCAMXjCmBDA5gGziEBGSObUkA%3D%3D%3D&bn=Courier%20Roket
              "• [Боевой курьер с призмой](https://s.orbis.zone/71hp)\n"  # https://coriolis.io/outfit/imperial_courier?code=A0p5tzF8l3das8f227272708080808402t1E1E27252525.Iw18SQ%3D%3D.Aw18SQ%3D%3D.H4sIAAAAAAAAA42SP0vDUBTFb9Mmtn1pQmJTi4p%2Fo6CD1LEgOAku7h39AA4FEToI6u4k4uTQD%2BDg6NDBwdFVcJDiB3AUEa33em6hD4qDyXA45Pxy373vhniCiH5cyOACYnoOUeXUJ4pacPGdIUrfc0SS421LnkCKDyWicOtDpNYNkTtcs%2FkhJEy%2FRKpz3yKJ5vXbAtFyewpknqct2RmRw5OqxwnIFyRS4M0RFHbekD%2F2RcTlpv30DFLyWaR8GREtqltSt6JuVZ14vD9e5P5VZEN7liK3bCVMSwVtwm3NEHk3FXQ6bKKUBSpngQzvWOha29G3ceMI4%2Bo9zj8HgPwsUIV3xyDTxriRSnpeRh78k4e8Z%2FMDiFMfiHi6HdPMY%2B19SKInpT38GjLJaxa%2FggSNT9xjV6%2BwyutjkXmCDRZmUURdrGtP1UmSmaxlJoX%2BPr%2FzFR%2BFzgIAAA%3D%3D.CwegjOIAwgTNICmBDA5gG0ScVcJlEA%3D%3D&bn=Multi%20PvE%20Courier
              "• Автор: <@270156067055468544>\n\n"
              
              # Автор Klemyr
              "• [Курьер Быстрый Боевой](https://s.orbis.zone/2jf5)\n"  # https://coriolis.io/outfit/imperial_courier?code=A0p5tzF5l3das8f2PhihPh080h00032tB41E276e2E.Iw18UA%3D%3D.IwBj4jQo.H4sIAAAAAAAAA3WRMUsDQRCFR70kl9xdLjkvMQQbNSo2QSGNINYWghZincbGSrAR0UKwtBAx2Ka0tLCw9AdYWFoECVYiKcRCRM2Mb05uiZJs8Rhmvp2ZfUucJKJuAvJ9BnFqNpHnskjeThEFxy8ilRbKMsTLhjyE2OtfIn67SlS8skDeA5dhLhpoF%2BJXPkXCDqTQ9IlKSk7tjIEc4bIh92MyuHGIwoMCyGimxQsKWVqvv6J%2B%2FSQiCV40V48gaV03c54nmtBoUqNpjWY0kiTXY9zf66DJbVukuvSOTjZvmk45SHLjDW86fQb00BIp6UxJ90Bbg6BMD5QaBDm8YqALNTvyWaVyksGmLq%2F93fTuEbc89vpks1zrk83xqpmwrSV9ZqD18LKLT1BXf3cJeM6QDUh2%2FgPJproyyuOx625uFhf068qRYUL%2Fzw%2FOdm4nQQIAAA%3D%3D.IwOgrA9AzBqQDBALBRBTAhgcwDZorPEaifEA&bn=Speed%20Wagon
              "• Автор: <@189334900405436416>\n\n"
              
              # Автор Andrew An
              "• [Исследовательский курьер](https://s.orbis.zone/3d64)\n"
              "• Автор: Andrew An\n\n"
              
              # Автор Tmtgrs
              "• [Торпедный курьер](https://s.orbis.zone/80tV)\n"
              "• Автор: <@514930529183989842>")
    embed.set_image(url='attachment://gutamaya-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Courier// КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Eagle
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Eagle // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Sidewinder
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="sidewinder", description="Список сборок для «Sidewinder»")
async def sidewinder(ctx):
    file = discord.File("sources\images\corporations\delacy-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Sidewinder",
        description="```Многоцелевой корабль производства Faulcon DeLacy. Его универсальность и сравнительно низка цена заработали ему популярность среди начинающих пилотов, но пусть вас не обманывает репутация Sidewinder как корабля для новичков. Данная модель — одна из самых маневренных на всём рынке.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value="• [DarkWinder](https://s.orbis.zone/4uji)\n• Автор: n/a")  # https://coriolis.io/outfit/sidewinder?code=A2p0u0F0l3d0s3f12j2j0200272725m1m166.Iw1%2FADJQ.Aw1%2BkA%3D%3D.H4sIAAAAAAAAA42QsU4CURREB3fRhV3AXQGJwURlgcTCxNLEgp%2Bw5xMoLCywoaImxMrCT7C09AM0saEjxspQUJNo9F7vkPgSjAWvmEzunDd570ICAN9Zk6%2BRSdj7UI27n6rpXQnQjHRcfm0S3L6rJi9bQDU1SDek6vJLkxKn5blJhfdr9z7Q6O1akyd7v%2BQSSh5CoNyvGDS1ofpy6vKrueVPr9aflTPXPzDJRaKaH8fAId0RXZOuRaeb0l0teXxTPTlfWFMgF66pYILtNuBTEr6vxj%2Ftzzwrya1N5qVJ0iM03LGcUJ1OQ4n%2BiZa3Ijl2%2FTfc%2BbPZ4kEdiOkSLi6l08LaZPEvOXHkxJF0qlg5P%2BCdwyMBAgAA.EweloBjEoUwQwOYBtYhARgtmuJA%3D&bn=DarkWinder
    embed.set_image(url='attachment://delacy-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Sidewinder // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Viper
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Viper // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Viper MkIV
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Viper MkIV // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Vulture
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="vulture", description="Список сборок для «Vulture»")
async def vulture(ctx):
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Vulture",
        description="```Создавая Vulture, Core Dynamics выжали всё возможное из своих технологий, оснастив компактный корпус корабля двумя большими гнёздами. Производитель также снабдил Vulture мощными маневровыми двигателями, благодаря которым корабль способен уклоняться от вражеского огня, одновременно нанося значительный урон, что делает Vulture крайне опасным противником.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор Artificial Intelligence
              "• [2 банки и дробовики](https://s.orbis.zone/cdyg)\n"
              "• Автор: <@232550259841171466>\n\n"
              
              # Автор HarrisonSould
              "• [Cтервятник для PVE](https://s.orbis.zone/7s3j)\n"
              "• [Стервятник на дробашах Хадсона](https://s.orbis.zone/7s3o)\n"
              "• Автор: <@270156067055468544>\n\n"
              
              "• [Vulture с пучками](https://s.orbis.zone/22rt)\n"
              "• Автор: <@269516916631142411>\n\n"
              
              "• [Вультура с улучшенной плазмой](https://s.orbis.zone/29m0) от Paffoc\n"
              "• Автор: Paffoc\n\n"
              
              # Автор Kawaiski
              "• [Стервятник на дробашах](https://s.orbis.zone/7s3q) от Kawaiski\n"  # https://coriolis.io/outfit/vulture?code=A4patfFalddksif31t1t04040404B21K1J6b2525250y.Iw1%2FgDJQ.Aw18cQ%3D%3D.H4sIAAAAAAAAA42RvS4EcRTFz87ssvOxO2bMrCUSX4NQaTeRqCQajedQKMgqttgHUIgIjcIjKBVbKryARCGeQK2Qda9zJf5CNVOcnH%2FOb3K%2FIJMAPhuU8QUlOq8BrWEMpH267D4CypEHaE12HDmgNB8CINl%2BV%2B3cJsw96bj8mJKUH6r5G6WwvHtXB1aOZkj6MufI%2Fg%2F5XSkfFCRfmGhDeg4aUoJYVMPLFFgyt2xu1dyaOW3KgcPZPPxHysYp3%2FWpdWC2O1bVoAoUyp6Drm0jViQ1Kc9CVop%2B8%2F9RLLvu1xsbzCbJtk44ky1r4blNqFUFasu%2Bgw4pnrU2YSuMej5v80opjCxHvJ9msunwK2vsiba9OE%2FSXGYHKM3pdGUyr0wq%2Fn5fbD2AbVQCAAA%3D.CwegjOIAwgHNICmBDA5gG0ScVcJlEA%3D%3D&bn=Cruel%20Bitch
              "• Автор: Kawaiski")
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Vulture // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Challenger
@ships.command(default_permission=False, name="challenger", description="Список сборок для «Alliance Challenger»")
async def challenger(ctx):
    file = discord.File("sources\images\corporations\lakon-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Alliance Challenger",
        description="```Не что иное, как видоизменённая модель Alliance Chieftain с особым упором на ведение открытого боя. Корабль обладает внушительным количеством гнёзд для орудий, что делает его довольно грозным противником. Хоть Challenger и тяжелее своих «родственников», он тоже отличается характерной для Chieftain маневренностью. При этом корабль оборудован более прочной бронёй, нежели Chieftain, и потому способен дольше продержаться против превосходящих сил противника.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор Artificial Intelligence
              "• [PVE с рельсами](https://s.orbis.zone/cdxr)\n"
              "• Автор: <@232550259841171466>\n\n"
              
              # Автор HarrisonSould
              "• [PVE challenger](https://s.orbis.zone/3jrw)\n"
              "• Автор: <@270156067055468544>\n\n"
              
              "• [Challenger с призмой и улуч. плазмой](https://s.orbis.zone/1sld)\n"
              "• Автор: <@235835602317082625>")
    embed.set_image(url='attachment://lakon-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Challenger // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Chieftain
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="chieftain", description="Список сборок для «Alliance Chieftain»")
async def chieftain(ctx):
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Alliance Chieftain",
        description="```Alliance Chieftain не только представляет угрозу в бою, но и способен избегать огня противника. Lacon Spaceways обеспечили кораблю высокую манёвренность и впечатляющее вооружение, благодаря которому Chieftain может без труда постоять за себя. В трёх внутренних боевых отсеках можно разместить щитонакопитель, а также усилители модулей и корпуса.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор Artificial Intelligence
              "• [AX с щитами](https://s.orbis.zone/cdxx)\n"
              "• [AX с щитами и ремонтными дронами](https://s.orbis.zone/cdxy)\n"
              "• [PVE с плазмой](https://s.orbis.zone/ce3c)\n"
              "• Автор: <@232550259841171466>\n\n"
              
              # Автор HarrisonSould
              "• [Chieftain на пиратских лордов](https://s.orbis.zone/4clw)\n"
              "• [Chieftain исследователь](https://s.orbis.zone/3y2v)\n"
              "• [Chieftain с плазмой и рельсами](https://s.orbis.zone/3y2w)\n"
              "• [AX Chieftain](https://s.orbis.zone/3y2u)\n"
              "• Автор: <@270156067055468544>")
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Chieftain // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Crusader
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="crusader", description="Список сборок для «Alliance Crusader»")
async def crusader(ctx):
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Alliance Crusader",
        description="```Представляет собой видоизмененную модель корабля Alliance Chieftain, от которого отличается в первую очередь наличием отсека для истребителя. Crusader имеет три внутренних боевых отсека и место для экипажа из двух человек, что делает его идеально подходящим для практически любого сражения.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор HarrisonSould
              "• [PvE Crusader](https://s.orbis.zone/3jro)\n"
              "• [Crusader на дробашах](https://s.orbis.zone/3jrs)\n"
              "• Автор: <@270156067055468544>")
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Alliance Crusader // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Asp Explorer
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="aspe", description="Список сборок для «Asp Explorer»")
async def aspe(ctx):
    file = discord.File("sources\images\corporations\lakon-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Asp Explorer",
        description="```Часто продаётся в качестве идеального корабля для пилотов, подбирающих свой первый корабль для нескольких экипажей (Multi-Crew). Его большая дальность прыжка и широкий фонарь кабины с хорошим обзором заработали этому творению Lakon Spaceways популярность среди исследователей, но универсальность данной модели также делает его отличным вариантом для торговцев и боевых пилотов. Для Asp Explorer подходят посадочные площадки среднего размера.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value="• [ASP для начинающих](https://s.orbis.zone/cl82)\n"
              "• Автор: <@360125693729964043>\n\n"
              
              # Автор HarrisonSould
              "• [ASP Исследователь](https://s.orbis.zone/3oi8)\n"
              "• [Боевой АСП](https://s.orbis.zone/3oi9)\n"
              "• [ASP Майнер 3.3](https://s.orbis.zone/3oia)\n"
              "• [ASP Майнер пейнита](https://s.orbis.zone/3utw)\n"
              "• Автор: <@270156067055468544>")
    embed.set_image(url='attachment://lakon-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Asp Explorer // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Asp Scout
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Asp Scout // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Assault Ship
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="fas", description="Список сборок для «Federal Assault Ship»")
async def fas(ctx):
    file = discord.File("sources\images\corporations\core-dynamics-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Federal Assault Ship",
        description="```Многие из клиентов Core Dynamics считали, что их десантные корабли должны выполнять более определённые задачи. Ответом на эти запросы стал атакующий корабль. Он лучше приспособлен для боевых действий, чем исходный вариант. У него выше маневренность, а вооружение мощнее у расположено удачнее. Ради этих модификаций пришлось пожертвовать вместительностью, вследствие чего он менее универсален, но лучше справляется со своей специализированной ролью.```",
        colour=0x2F3136,)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор Klemyr
              "• [Бронированный FAS с торпедами](https://s.orbis.zone/2_we)\n"
              "• Автор: <@189334900405436416>\n\n"
              
              # Автор HarrisonSould
              "• [FAS 355](https://s.orbis.zone/3jti)\n"
              "• [FAS Explorer](https://s.orbis.zone/adp)\n"
              "• [FAS AX](https://s.orbis.zone/42ww)\n"
              "• [PVE FAS](https://s.orbis.zone/3jtp)\n"
              "• [ФАС с мультиками и плазмой](https://s.orbis.zone/3jts)\n"
              "• Автор: <@270156067055468544>\n\n"
              
              # Автор Artificial Intelligence
              "• [PVE с рельсами](https://s.orbis.zone/cdxu)\n"
              "• [AX с щитами и дронами](https://s.orbis.zone/cdye)\n"
              "• Автор: <@232550259841171466>")
    embed.set_image(url='attachment://core-dynamics-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Assault Ship // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Dropship
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Dropship // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Gunship
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Gunship // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Fer-de-Lance
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="fdl", description="Список сборок для «Fer-de-Lance»")
async def fdl(ctx):
    file = discord.File("sources\images\corporations\delacy-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Fer-de-Lance",
        description="```Fer-de-Lance — это тяжёлый боевой корабль производства Zorgon Peterson. За четыре средних и одно гигантское гнездо на борту корабль можно смело назвать серьезным противником, справиться с которым будет нелегко даже Anaconda и Federal Corvette. Если у него и есть недостатков, то это его узкая специализация. Покупателям не рекомендуется использовать Fer-de-Lance для какой-то другой деятельности, кроме боя.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор HarrisonSould
              "• [PvP Fer-Lance-De](https://s.orbis.zone/6vso)\n"
              "• [PvP Conduit Plasma](https://s.orbis.zone/6zyu)\n"
              "• [PvP Реверсный](https://s.orbis.zone/7s9w)\n"
              "• [FDL Explorer](https://s.orbis.zone/6vsg)\n"
              "• [FDL с многостволками](https://s.orbis.zone/6vsz)\n"
              "• Автор: <@270156067055468544>\n\n"
              
              "• [PvP FDL с двухпоточником](https://s.orbis.zone/2-k0)\n"
              "• [AX FDL](https://s.orbis.zone/20u8)\n• Автор: Equalizer\n\n"
              "• [AX FDL v2](https://s.orbis.zone/5x7m)\n"
              "• Автор:  <@305091226611351572>")
    embed.set_image(url='attachment://delacy-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Fer-de-Lance // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Keelback
# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Keelback // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait MkII
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="krait", description="Список сборок для «Krait MkII»")
async def krait(ctx):
    file = discord.File("sources\images\corporations\delacy-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Krait MkII",
        description="```Переделка Krait Lightspeeder, который изначально производили Faulcon DeLacy в 3100-х. И хотя новинка крупнее оригинала, у них сходные характеристики, скорость, манёвренность, а огневая мощь превышает уровень защиты. Также в корабле присутствует отсек для истребителя и место для экипажа из двух человек, благодаря чему он представляет собой хороший вариант для тех, кому требуется многофункциональный корабль среднего веса.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор HarrisonSould
              "• [Исследовательский Krait](https://s.orbis.zone/3qky)\n"
              "• [PVE Krait](https://s.orbis.zone/4z1s)\n"
              "• [Krait с плазмой](https://s.orbis.zone/3uxf)\n"
              "• [Krait на дробашах](https://s.orbis.zone/3uxi)\n"
              "• [Krait AX](https://s.orbis.zone/3980)\n"
              "• [Krait майнер 3.3](https://s.orbis.zone/3uxn)\n"
              "• [Майнер пейнита](https://s.orbis.zone/3uxs)\n"
              "• [PvP Krait v2](https://s.orbis.zone/4c1d)\n"
              "• Автор: <@270156067055468544>")
    embed.set_image(url='attachment://delacy-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait MkII // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait Phantom
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="phantom", description="Список сборок для «Krait Phantom»")
async def phantom(ctx):
    file = discord.File("sources\images\corporations\delacy-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Krait Phantom",
        url="https://elite-dangerous.fandom.com/wiki/Krait_Phantom",
        description="```Krait Phantom считается универсальным судном для любого пилота благодаря вместительному грузовому отсеку и довольно-таки внушительному арсеналу гнёзд. Ему хватит огневой мощи, чтобы сдержать натиск более крупных целей, а по своей скорости он может соревноваться с кораблями заметно меньше собственного размера — во всяком случае, при полёте по прямой. Ещё одно достоинство модели — восемь внутренних отделений, которые пилот может обустроить по своим потребностям. Корабль куда быстрее и легче своего собрата, Krait Mk II, хоть и уступает ему по вооружению.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор Artificial Intelligence
              "• [Pathfinder](https://s.orbis.zone/cc4g)\n"  # https://coriolis.io/outfit/krait_phantom?code=A0p5tdFflid3ssf5----02---3c1O0s049qv6432i3w.AwRj4y2HTI%3D%3D.Aw1%2FAjGBMKUA.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf85wBXWQMkOOY8%2B%2F9f6AJQu5jKr%2F%2F%2F%2FzP9E4PLlwAJfpCoiNzv%2F%2F9FF%2FAzMEhsYGFgUC4QB5rE%2FE8KrrICphJsk0iNKFDlHaDMf5Z%2FhjBF%2FBVvgPJn7gEtYf1nBdfaCCQ4QQZyGQgyMCiCDFECEaogQo3nH1A5278EVEMOPPj%2FX8%2FmG1CK5x8nFvPF%2FvnAzc8BSYHUCoHkRVb8BfoE5DSJhA9AleL%2FYmEqhQTUGRhMO4SBrv7PAAcABpPtZloBAAA%3D.EwegLCAMUgzKAOEBTAhgcwDbJCAjJITNJEA%3D&bn=Pathfinder
              "• Автор: <@232550259841171466>\n\n"
              
              # Автор HarrisonSould
              "• [Phantom исследователь](https://s.orbis.zone/48_o)\n"  # https://coriolis.io/outfit/krait_phantom?code=A0p0tdFflid3ssf4----02---3c0s1O0443v62i3x3w.Iw18gDBxA%3D%3D%3D.EwBj4zQRkkg%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8Zw9XWQ8kOI5wMjDw23z7%2F19sAT9QnumfGFy%2BDEjwq%2Fz6%2F1%2FkDZAQBclLbGBhYFAuEAeqZP4nBVdZAVMJtkmkRhSo8g5Q5j%2FLP0OYIv6KN0D5M%2Ff%2B%2F%2F%2FP%2Bs8KrrUFSHCCDOQyEGRgUAQZogQiVEGEGs8%2FoHK2fwmohhx48P%2B%2FHsjN%2F3n%2BqWExX%2BSfD9z8Qgao%2F4RA8iIr%2FgJ9AnKaRMIHoEqxf7EwlUIC6gwMph3CQFf%2FZ4ADAK%2BCCj5aAQAA.EweloBhBGA2EoFMCGBzANokMK4fiIA%3D%3D&bn=Phantom%20Explorer%20V1
              "• [PVE Phantom](https://s.orbis.zone/42yo)\n"  # https://coriolis.io/outfit/krait_phantom?code=A4pptkFflidussf57l7l0s0s04040404B11K1K1K2t1F1F273w.Iw18WQ%3D%3D.Aw18WQ%3D%3D.H4sIAAAAAAAAA42RL0%2FDYBCHj64t%2FbvSZt0WSBiMgoOUBENCCIYEg0NMYnAIBCQTIEiQKAQYBB8AgUQg%2BRAIQtAEhSJk3PG7JbyBma3iyZv%2Bnrte3yN2iejbAXoXQHhnE8URi6R7OGVnbyLFikckY7yuZkXNE8B77YkkGy2i%2BgxeZlooFtdNu0MgKb5Eau9AfpMQNVWaO2jArPCkMbu%2FZnYfEtWOc5jPSMTmZZUszctP5DqOOLxmSk8BX0sDxayirdPP60cWyhRNXN7932TnQ2SpienF447pFAG21judKSL3Nsak%2FSH8UaTgjzQNDObhkDziLZNf6R76K1AU5wHyeEhe5U2TX%2BufatesPMJNPvpEracqpGQUaYK3jbQPWHpTri4uXMWe0xcgV7N4GIfe4EWjX%2BpgbehVbZzqqehi7SI0%2BPwAGDQcNHgCAAA%3D.CwegjOIAwgzATNEBTAhgcwDbJOK%2BkYog&bn=PVE%20PHTM
              "• [AX Phantom](https://s.orbis.zone/42wx)\n"  # https://coriolis.io/outfit/krait_phantom?code=A2pptkFflidussf50H0H0Hx80404xs02B12d2d2d292929m3m1.Iw18WQ%3D%3D.EwRgDBlVLuVA.H4sIAAAAAAAAA43QsUoDQRAG4D8Xo8a75HKbuzNIIFFPBau0goiNpb0PYWGhYKGgnbWFlYWPYKdFSskzWIj4AJZWEmf8R3BBq73iZ7j9dpYZyByArwZjes2IxxHQukiA7ICVe4yB6qMGaE12TNZNnjPm36aq6e4AKIf86e5niCIpfbtjRlp9qubvjOIuBXqGVo8WKeuy5OXpr%2Fx5Lj8rKF94og3Z9uiS0TS0YLFssZKI6pq1Wx9l5InseX5rPa2JG52w3VMTGDy3iVohKHWdDZ5ddYG%2BhXZk3986ZEQ9Tj9r48RbnD57ZRR2tRpzoZrJpuc3ttYHlu1hn9IqZ8uorFIXLLvBMv8vJ15OvLRKi2BZBkvF3%2B8bDD2Eo2MCAAA%3D.CwegDCBM4gzNECmBDA5gG0SEBGM%2BYIwg&bn=AX%20Phantom
              "• [PvP Phantom Prisma](https://s.orbis.zone/47tu)\n"  # https://coriolis.io/outfit/krait_phantom?code=A4pptkFflidussf52a2a2aih04040204p11K5i5i29292t6b3w.Iw18WQ%3D%3D.MwRgDBldkiBMCg%3D%3D.H4sIAAAAAAAAA4WSO0sDURCFx7yTzcPdvCVo1NWIoKSwEQQrQQtbbS3UKkUKlTQWCoK2KRTEIj%2FB0sJKtPAFgoVBREQrxSKV%2BIh3PBPIRSHgFoezs9%2BZuXvvJeUhom83pF6GWLsvzKGgYjYXXET2iI%2FI2IfjNjUupFPIVUjE%2FmRODASIfHeIs0MldKel5veURGOdX8zxcoSot5gE6VQdmizJzAOjiUunWCUKyGVdPzJH5mrM7FajOrAG6ZP19W%2BZRH5xAXHd4nrEsUfNNXHr9gFNSq%2FMw2Nv6ORTs7rTYnN0Y6qUKP3RD61VQfr%2FIZ80GfiHPNOk8Yuc%2F0vm35nTzyA5qCY0tCdQfhm7U8V76thP1HUZJjKlsS1iiHBITerMDqRLqmYRO2Kv44AMcRy22nMob2J3MyIcaTnpRk86bzGpXU3rTAGSkmr8FKQjVWf2yHmb97gk9qEXmVE4ttSUZFyS2YC0SffsCk7WW8Gh5K5AcrQlVNDQiUAxNainb8uKK7hU4WwGM49QtEUMEY6roT9k%2BALWzGGJ9gwyhjhOqoxADvkPWUSH3MFg444ytXp%2BAOfN7nUuAwAA&bn=Scavenger
              "• [PvP Phantom Bi-We](https://s.orbis.zone/7s98)\n"  # https://coriolis.io/outfit/krait_phantom?code=A0pktkFfliduspf52a2a2a2a04040402B11K5i5i29292t6b3w.Iw18WQ%3D%3D.MwRgDBldkiBMCg%3D%3D.H4sIAAAAAAAAA42Sr0tDURTHz%2BZ%2B721v7%2B73GDr1ucGCWAXBpGKRNY0LYhDDgsqKMIOgYFrQYljwDzAaDAY1mATLgkG0GhZE8Nc5njO3i4PBfOHLl3s%2B937vuecBegHg283yVWcJXjgBQjUDwFphp86DAParA4AcOKvJHRbflR%2FAnHkjSjRMrjsxoeubLKb9QZQ6cwHEhj%2BJ4nWGxitJJocwo8kqdEJ%2B8QdejDWiDLnU%2FRORWW4RkRun9YZdlgkDifIHFoBfXEDcqLgxceTBchc3qy9E6vKRaFJuSj5c1ietdaPbqbIE6fc8a6vJpH8A%2BazJwADyVpPBP%2BQqS7HUg6cjBb69gfMaOpaJVLgx6zDAcxBHIVzorZ96uM8SP7ElLiVjscVRGOc0eSKPISFqaqsDjTTDDJlKUmGf3zwrQhFc0rvWZZdM15Lz7fb0FC5K3SX1PRaHnJXb5jl5G%2FzEhTv%2BoSjaF9rQ0LVAMSzqpCPp5IZtOJflOHFKgm1xFP83mcRsN9iQxlJSyrRnT9Dv%2BwGtabxEAQMAAA%3D%3D.CwegDCBM4qEKYEMDmAbeIQEYy5hMIA%3D%3D&bn=Scavenger%20Bi-We
              "• Автор: <@270156067055468544>\n\n"
              
              # Автор Andrew An
              "• [Бронированный исследовательский фантом](https://s.orbis.zone/46rl)\n"  # https://coriolis.io/outfit/krait_phantom?code=A00BtiFflid8ssf4------08083c0s1O0sv62ip4273x.Iw18gDM1kA%3D%3D.AwRmwFnadmqA.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf6JwZXWQYk%2BFV%2B%2Ff8v8gZIiC7gZ2CQ2MDCwKBcIA5UyfxPCq6ynAFqCFi5xB2goMgvEaAiln%2BGMEX8FW%2F%2B%2Fxc6c%2B%2F%2F%2F%2F%2Bs%2F6zgWluAhCpIlxrPv%2F%2F%2FOQ8AdXG5AG1SBIkpgYj%2FbP8SUA058OD%2Ffz2bb0Apvn%2BucJPmgORBVgsZlAJdeoSTgUH%2BBh%2FQEfzEKBL9FwtTJCSgzsBg2iEMFBX75wPXWgjSCrJVCOQIkRV%2FgWECMkki4QPQJeL%2FNOEqpwEJPoMfQJULQI78z4AAAKcyXI2KAQAA.EwegLCAMUgjAbDApgQwOYBskjpPNpIg%3D&bn=%D1%83%D1%81%D0%B8%D0%BB%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20phantom%20%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%20(%D1%81%D0%B8%D0%BB%D0%BE%D0%B2%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%B0%D0%B6%D0%B5%D0%B9)
              "• Автор: Andrew An")
    embed.set_image(url='attachment://delacy-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Krait Phantom // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Mamba
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="mamba", description="Список сборок для «Mamba»")
async def mamba(ctx):
    file = discord.File("sources\images\corporations\zorgon-peterson-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title='Mamba',
        url='https://elite-dangerous.fandom.com/ru/wiki/Mamba',
        description='```В основу разработки Mamba был положен прототип гоночного корабля, так и не увидевшего свет, поэтому нет ничего удивительного в том, что эта модель является одной из самых быстрых из находящихся в производстве. При этом одно гнездо четвертого класса и два — третьего обеспечивают ему достойную огневую мощь. В сочетании со скоростью это позволяет пилоту нанести молниеносный удар и исчезнуть до того, как цель откроет ответный огонь. Безусловно, судно во многом напоминает Fer-de-Lance — другой корабль производства Zorgon Peterson, — однако Mamba легко обгонит его при полёте по прямой, пусть и не обладает такой же манёвренностью.```',
        colour=0x2F3136)
    embed.add_field(
        name='СБОРКИ',
        value=# Автор HarrisonSould
              '• [PVE Mamba](https://s.orbis.zone/6v9z)\n'  # https://coriolis.io/outfit/mamba?code=A2pftfFalidpsif37o7l7l0p0p040404040400B21J6g2o273w.Iw18aAMQ.Aw18WQ%3D%3D.H4sIAAAAAAAAA42Suy8EURTGz%2B7OjJ2d187sMwjBIBpZpUolOlFOuZ1CoyBRkNCpRWSLLbZQKhQKhdIfoFSoREShUIgIu%2Bc4Z2KuRzxmii%2Ff5PzOd899APYBQE9n6e6xWGdZAGfbBvAjdsGpBRA%2BZgAog3NCakJuseQvuNNrPBNVbxinLFZV0hqLF74Qle9ZKh0PoH7MnWOrNSZz2K%2FIjYSMVypvVpi84gppOJMs5zUfuH5yTUQ6zqrWHRbTRqLCvg8wIm5U3Li4CXFkYPNrSPuWaFpmpjxGKinHoskQejQAYBw5PGk8hPkJsn%2BDCmkgC5cVNMTyvW7%2FU3dwIalbhwZvZ%2BmVyBdXPzf5isSRi%2FMqpC17ltagsf4ODV%2B6DHlpoGIayP%2BYqdv6c7AA5WB6cs6wW%2BKk4iTA4B3%2FUwkXVciKrCSPxZeQMH4sNZxS9QMWV24v6DzxFRL88L0B9j%2FH3NECAAA%3D.EweloBhAOEoUwIYHMA28QgIwV3fEQA%3D%3D&bn=PVE%20MAMBA
              '• [PVP JellyFish](https://s.orbis.zone/6v9x)\n'  # https://coriolis.io/outfit/mamba?code=A0pktfFalidpsif31u1u1u2921040404040404p21E1E276b3w.Iw18WQ%3D%3D.EwRgDBld3mQ%3D.H4sIAAAAAAAAA4WSMUsDQRCFxyR3ueSSnHcmMSoq6hlIIwnYCIKFiDbWprSwESxSKAhiIVhaigpa%2BAMstLO0CNgISRkhiIWVWItonHHm5BYTFrziMbfzvbe7wwKaAPBtsNizFkA6hUSuFQfwDl%2BJ%2FDZ3qA8XBIqxdPZZrCb3nfIHUf4lxf0I5sOQzjaL438SFa6Zz459EeX2HYCp2iCTURxW5B6Ld2uHuOyU3cwxyetAMayEpLP7RuQ9PBGRgXPKf8AyLcctHrsACamSUk1INSkVmbjeHXL3TDQz%2F85JFlZVEt8BjOURAPMqzfvLSUYrHYYSvVBJAyV7oUUNZOOagjbCiwd3NmSOQ%2FdFPm7qT1JUkqpdSZTGJdW%2FkJDyDl%2Bsyf%2BFegJgvJ4BcGV6vogdzDGj9bSVp6HxOD2eAA%2BMv54We6j%2Fn%2BCWJtjVehrKc67xeLiiPKeyWpMXKuIfJbk%2FgKuqv8WSO%2BOQSIGHbsoLdB95kv5NXN43V5THksJPWDIyfu9SngSB5vsBTrLR7iEDAAA%3D.EweloBhAOEoUwIYHMA28QgIwV3fEQA%3D%3D&bn=JellyFish
              '• [PvP Multi-Cannon](https://s.orbis.zone/6v9s)\n'  # https://coriolis.io/outfit/mamba?code=A0pftfFdlidpsif37o7l7l2424040404040404p21E1E276b3w.AwRj4yvI.EwRgDBld3mQ%3D.H4sIAAAAAAAAA42SP0sDQRDFJ3%2FN5S4578zFoKCop2AjEWwEwUqwsU%2FpB7BIoZAihfZWImphkQ9goZ2FhUVKQUuFIH4ASxHROOObkyxREriFfczxfm9vllniESL6zkC6RxD7JklU2HeIvBoq%2F9omCt8SRJLgdUM2Ibm2ReSuvYuUWy78JJeNvwtxw0%2BR0tSXSKB%2B5TJNNFcfB5niCUM2emT0p1IzANmBI2le7kFu4xX%2B3bOIZHjVRA8g8w6LLBx7RJZWea1mtJrVSrK8%2FfeQ2xeRJe1ZclwzJ2FTWpvI1CaJshcFdBo1YfVBzjAoHwey40BOH5QbBhV4w0DnEL%2B6h9s94LuiE5luFzE7vVGoYqtIcWCmYzL3AzLuv0yER8HfzCMyMhoH8uJAPm8a6FSbqGOKnkp4mIc%2FxlvG34EEZ0glK12RrL4s7ymF7q%2FwmO0VVFLmRYOfQIrVD4y%2FpZMXGrB%2BAOTWbW8IAwAA.EweloBhAOEoUwIYHMA28QgIwV3fEQA%3D%3D&bn=PvP%20Multi%20SF
              '• Автор: <@270156067055468544>\n\n'
              
              # Автор Andrew An
              '• [PvP Duel Multi-Cannon](https://s.orbis.zone/7s05)\n'  # https://coriolis.io/outfit/mamba?code=A4pktfFalidpsff37o7l7l2929040404040404p22b1F1E1E25.AwRj4yvI.EwRgDBldMUA%3D.H4sIAAAAAAAAA42SvUsDQRDFJ19nkkvucmcSEz%2Fwa1UIKGkDgpVoI6QzrWBpYaHYKJg%2BhYhiY2FhaWFpEaz8IyzEv8BaROOMbw6zIFjcFY%2FHzu%2Fezu4O8QgRfWcgg3OIe5YgKp4WiIIjuPDBJTL9JJEkeM2SJ5DsU47IX30Xqd74qCe5ausHEN98ipTfIBWt1%2B7TRPP7YyBTPD4kIyjapHxcAfSCRclwyyZ1IbkCi%2BQvAqJZdXPqFtQtqhOHdxRPQULNX2l%2BiNSjUpY7NglHorRul%2BlMEDl3RbQTbZeLA%2BXjQC5vW2gX0mjT7xVGB6uXlgAV4kBF3rTQlT6LHjdQMb086h6v2%2Fq13qP%2BGjYPEaLPMv3sAfLjQKU4UBAHCnnjb8%2B3Dsj2FxpXF5FGnYzyliX3IMnaQMTRAXFbeMbgFVLRTNPHdEqZG0PcfYR6M5OA1IU6WUad1HjZZl4qOYVMT%2FsM1JmezqjQP98PUypCHAMDAAA%3D.EweloBhAOEoUwIYHMA28QgIwV3fEQA%3D%3D&bn=Duel%20Multi-Cannon
              '• Автор: AndrewAn')
    embed.set_image(url='attachment://zorgon-peterson-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Mamba // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Python
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="python", description="Список сборок для «Python»")
async def python(ctx):
    file = discord.File("sources\images\corporations\delacy-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title='Python',
        url='https://elite-dangerous.fandom.com/wiki/Python',
        description='```Многофункциональный корабль от Faulcon DeLacy, Python предлагает заманчивый баланс манёвренности, огневой мощи и брони. Благодаря пяти гнёздам он способен дать отпор большим кораблям, таким, как Anaconda или Imperial Cutter, в то время, как его мобильность позволяет справляться с мелкими судами, не задействуя турели. Python также обладает вместительным трюмом, что делает его более подходящим вариантом для тех, кто ищет грузовой корабль, способный принять бой.```',
        colour=0x2F3136)
    embed.add_field(
        name='СБОРКИ',
        value=# Автор HarrisonSould
              '• [PVE Python](https://s.orbis.zone/6v8x)\n'  # https://coriolis.io/outfit/python?code=A2pktkFflidussf51u1u1u272704040404B1053c04Ce1Pv66g2i3w.Iw18eAMQ.Aw18RQ%3D%3D.H4sIAAAAAAAAA42SsUvDUBDGzzaJadI2TWhrVETUqKAgCi4FwUnsInQRO%2FoHODgodNBBcOwkgksHB0cHRwdH%2FwBHB3F0kI7ioPXO7wI%2BqFMyfBzv%2B727d5cjdojox4YMLiD%2BuktUKrJI6I4SRefvIskLbBnhTUOeQtzHAlGw8SlSvw7g57hu%2FCNIkHyJVPuQmvrxnUU0dzgGMs8Thuz8kdG9T1Q9qYFMy1m8plBe%2FeYH%2FN6biNjcMFfPIAV9qXcZEs1oNKvRvEYLGonD%2B8NJOn2RFS0nLu%2BaTEUIVRaJLJVIHxk%2FofupeACykJn0MpM%2B7xkSA6elFiQdQdr9uN5ZVpEitw2pfVj6ers9SeTcljDRdFgl3jJQT5vV02j1GOn0L00%2FlwGVs0ABbxvoSvfhBvsRtL6xDxqlZKKRVLg5TKZLo5J0Pfgh7xj%2FAJLTxh3dAr%2BBRsJXSE1rJg8Yiwj9%2F34Bw5sbVpsCAAA%3D.EweloBhBmUBYAcICmBDA5gG2SEBGCQkKEoA%3D&bn=PVE%20Python
              '• [Python исследователь](https://s.orbis.zone/3qkn)\n'  # https://coriolis.io/outfit/python?code=A0p0tdFflidissf5-----02---3c11-1O--43v62i.Iw1%2BgDBxA%3D%3D%3D.Aw18eQ%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUj8mQQkuPcwMTDwNvAwMAhGAFlCO7gZGFS%2BMDIw%2FGf8Zw9XWQ8kOI5wMjDw23z7%2F19sAT9QnumfGEieGSRfBiT4a%2F78%2Fy%2FyAEiIanAxMEgoAGWUwSqZ%2F0nBTaoAqVT59f8%2F2CaRGlGgyjtAmf8s%2FwxBilhA8gkfgPJbHv3%2F%2F5%2F1nxVcawuQ4CwQZ2DgMhBkYFAEGaIEIlRBhBrPP6Bytn8JMOX8FW%2BAhhx48P%2B%2FHsjN%2F3n%2FqaFKnbkHFBX%2F5wM3v5AB6j8hkLzIir9An5ziALoP5Jz%2Fkv%2FiYSqFBNQZGAwd5IGu%2Fs8ABwBG7vn8WgEAAA%3D%3D.EweloBhBmSQUwIYHMA28QgIwVyKBQA%3D%3D&bn=EX%20Python
              '• [Питон для Robigo](https://s.orbis.zone/6v8w)\n'  # https://coriolis.io/outfit/python?code=A0p0tiFflidsssf5-----02---mdmdmdmdmdmcmbmbma24.Iw18eAMQ.EwRgDBldK7bzEA%3D%3D.H4sIAAAAAAAAA2P4x87AwPCXFUhw72FiYOBt4GFgEIwAsoR2cDMwqHxhZGD4z%2FxPCqboTwUDVIpf5df%2F%2FxJ3gIIipsJARf8ZGACVmo8zTQAAAA%3D%3D.EweloBhBmSQUwIYHMA28QgIwVyKBQA%3D%3D&bn=Economy
              '• [Питон на дробашах](https://s.orbis.zone/4b0w)\n'  # https://coriolis.io/outfit/python?code=A4pptkFflidussf51u1u1u7e7e02040404B15n1K2d372b296g2i3w.Iw18eAMQ.Aw18RQ%3D%3D.H4sIAAAAAAAAA41SPUsDURDcfJrkklzuzJcSSTQXg6KiZRqxEYJgIwiW%2FgALC4UUCtqIiKVgkyI%2FwU6LlBaWlhYiVlbBKkiQuOtsIA8FwVwxzN3M7b7Zt8RjRPQVAlhtP1HiJE7k7IC5dxaR1%2FURiY9X1RQA9I8Bkde%2BiL1WJMqW8NG9CcLk5%2BywUv8AYHufIukOINOyifJqKu%2Fn4AzwpHE2hs5Bu%2FRRBs5nKBLklWFPu96F3nwTkRDXzK%2BngGicRWJXDtG0shllFWWzyiTMu7%2BLNDoiS9pOIrxlKl0AAg%2BAuQbeg6kq0UQeESU6iik2isnibWPChIlUGuiuziT%2FiGuYGjjjIzsTXBmmo%2FNx6GoqKJMkr5siTU2vM3WXD%2FH%2FfZSo%2BJSEyea6MV3rAujgHAXvMgY99Y%2Fu8KbR9wB%2BPVVY79mq4VDOCyCjnbw2ziwub5gtOgP4Wh%2FYIr2MQaaqrlK510OwNM%2BbpbwFJksFlFPm6ip5yiTLi8a0gMZJjego8941Xe6HXjW6Ms%2BPIiL01%2FMN9xfwbRADAAA%3D.EweloBhBmSQUwIYHMA28QgIwVyKBQA%3D%3D&bn=Python%20Na%20drobashah
              '• [Питон на дробашах Хадсона](https://s.orbis.zone/6v8_)\n'  # https://coriolis.io/outfit/python?code=A4pktkFfliduspf5papapa272704040404B13c1K1K2d2b296gv62i.Iw18eAMQ.Aw18RQ%3D%3D.H4sIAAAAAAAAA42SP0%2FCYBDGj1IQaGlpQ4H4J%2F6rkhg1ODI5mbA4mjAyOzlo4qCJH8DJODL4ARzcdGD0Azg6GCfjZIwDgzF45z3EvmEQQ4cnT3q%2Fu%2FeetyWeIqLvjMrgQsXpWUTFM5coaKsL7xyiuJ8ikhRvg7RBnqrkHrTTb3yKVF4UF4srZtKhih9%2FiZTfVKIrn6h2o53LB1Ul0zxtyOOEHJ5UPomUfNKK2LwFKI16q6%2F17quIZLiZtOZdFilcBkSLcEtwK3CrcJLlTrKu3%2Fn47d%2FEupLjPXM%2B0lOpTmRDQuxXQ7C52kDJ%2FAjp%2FksWJiYdbhsS6Wykz7RniLLXRb2iYXp3BHLHQUXeMVAXOfE2bBzpcfd5ovlHTyFvEsjnVgI5uMIAEp8XtFQaXwp414zeV7GQL4vv7DQ1WfCsEmF%2B3NP0EvGamXSr6i3MKgQX4geJ4aTCGwZa13Ee1g3g4ndsWh2p100dLrZ0iAj98fwAA%2Fj9yOUCAAA%3D.EweloBhBmSQUwIYHMA28QgIwVyKBQA%3D%3D&bn=Python%20Na%20drobashah%20Hudsona
              '• [Майнер Алмазов](https://s.orbis.zone/6v8u)\n'  # https://coriolis.io/outfit/python?code=A0pftiFflidussf52m2m2m--04040400050505CeCe32P9401l2i.Iw18eAMQ.Aw18RQ%3D%3D.H4sIAAAAAAAAA2P%2BJ8XAwPCXFUjwq%2Fz6%2F19oBzcDg0iNKAODxB2g4P%2F%2FDABJ8pCXIgAAAA%3D%3D.EweloBhBmUEZgA4QFMCGBzANikI4SEhQlA%3D%3D&bn=Python%20Miner%20LTD
              '• Автор: <@270156067055468544>')
    embed.set_image(url='attachment://delacy-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Python // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Type-6 Transporter
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="type6", description="Список сборок для «Type-6 Transporter»")
async def mamba(ctx):
    file = discord.File("sources\images\corporations\lakon-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Type-6 Transporter",
        url="https://elite-dangerous.fandom.com/wiki/Type-6_Transporter",
        description="```Type-6 Transporter производства Lakon Spaceways становится для многих независимых пилотов следующим шагом в их карьере после универсального Cobra Mk III. При должной оснастке корабль обладает достаточной вместимостью для успешной торговли стандартными предметами потребления и не подходит только для транспортировки редких предметов на дальние расстояния. Однако боевые возможности Type-6 довольно ограничены, и пилотам, деятельность которых сопряжена с конфликтами, рекомендуется улучшить щиты и корпус данной модели.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор HarrisonSould
              "• [Type 6 для робиго](https://s.orbis.zone/6v8r)\n"
              "• [Майнер пейнита](https://s.orbis.zone/6v8p)\n"
              "• Автор: <@270156067055468544>")
    embed.set_image(url='attachment://lakon-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Type-6 Transporter // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Anaconda
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="anaconda", description="Список сборок для «Anaconda»")
async def mamba(ctx):
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Anaconda",
        url="https://elite-dangerous.fandom.com/wiki/Anaconda",
        description="```Гордость верфей Faulcon DeLacy, Anaconda — это универсальный корабль, способный перевозить крупногабаритные грузы и обладающий огневой мощью. Он настолько хорош, что некоторые небольшие флоты используют его в качестве фрегата или лёгкого крейсера. На данную модель также можно установить стыковочный отсек.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор HarrisonSould
              "• [Универсальная Анаконда](https://s.orbis.zone/3oib)\n"
              "• [Анаконда для пве (с призмой)](https://s.orbis.zone/3jsn)\n"
              "• [Исследовательская когда прыжок 78.62 св.л.](https://s.orbis.zone/46xa)\n"
              "• [Майнер алмазов](https://s.orbis.zone/6eta)\n"
              "• [Анаконда майнер 3.3](https://s.orbis.zone/4d75)\n"
              "• [#DEVYNATION](https://s.orbis.zone/3kmf)\n"
              "• [AX Conda](https://s.orbis.zone/396w)\n"
              "• Автор: <@270156067055468544>\n\n"
              
              "• [Исследовательская Конда полный фарш](https://s.orbis.zone/1hlo)\n"
              "• Автор: <@513702986858364931>\n\n"
              
              "• [Конда с прыжком 80,45](https://s.orbis.zone/2put)\n"
              "• Автор: <@300234139750105088>\n\n"
              
              "• [ПВЕ, пучки, многостволки](https://s.orbis.zone/3oif)\n"
              "• Автор: <@259786273475002368>\n\n"
              
              "• [На миротворцах с пылесосом](https://s.orbis.zone/4zxc)\n"
              "• Автор: <@344735291384528898>\n\n"
              
              "• [Bliz 2KDPS](https://s.orbis.zone/6o54)\n"
              "• Автор: <@283578404274700289>")
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Anaconda // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Corvette
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="corvette", description="Список сборок для «Federal Corvette»")
async def mamba(ctx):
    file = discord.File("sources\images\corporations\core-dynamics-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Federal Corvette",
        url="https://elite-dangerous.fandom.com/wiki/Federal_Corvette",
        description="```Один из самых мощных кораблей на рынке. Мало кто способен составить конкуренцию Federal Corvette с его семью гнёздами в плане огневой мощи, а с учётом размеров это ещё и на удивление манёвренное судно. Несмотря на сравнительно небольшую дальность прыжка, Corvette является пределом мечтаний для множества независимых боевых пилотов, а невероятная мощность делает его одним из самых грозных кораблей галактики. Для Federal Corvette подходят посадочные площадки большого размера.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор Artificial Intelligence
              "• [PVE на пулеметах](https://s.orbis.zone/ce3f)\n"
              "• [AX с призмами](https://s.orbis.zone/ce3i)\n"
              "• Автор: <@232550259841171466>\n\n"

              # Автор HarrisonSould
              "• [PVE фит на лазерах](https://s.orbis.zone/84KS)\n"
              "• [Корвет на многостволках PVE](https://s.orbis.zone/84L4)\n"
              "• [Корвет с плазмой для PVE](https://s.orbis.zone/84L8)\n"
              "• [Дальнобойные пульсы + щит в резисты PVE](https://s.orbis.zone/3uwy)\n"
              "• [PVP Corvette](https://s.orbis.zone/43bn)\n"
              "• Автор: <@270156067055468544>\n\n"
              
              # АвторAndrew An
              "• [Корвет исследователь](https://s.orbis.zone/3kn-)\n"
              "• Автор: Andrew An\n\n"
              
              # Автор Painbeaver
              "• [AX Corvette II](https://s.orbis.zone/1gg5)\n"
              "• Автор: Painbeaver\n\n")
    embed.set_image(url='attachment://core-dynamics-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Federal Corvette // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Cutter
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="cutter", description="Список сборок для «Imperial Cutter»")
async def mamba(ctx):
    file = discord.File("sources\images\corporations\gutamaya-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title="Imperial Cutter",
        url="https://elite-dangerous.fandom.com/wiki/Imperial_Cutter",
        description="```Гордость верфей Gutamaya — это грозный универсал. Его брони и защиты достаточно, чтобы выдержать практически любые атаки, кроме разве что самых масштабных. Прибавьте к этому целых семь гнезд — и все это превращает Cutter в серьёзного противника в бою, в то время как его немаленький грузовой отсек также делает корабль хорошим вариантом для торговцев. Для Imperial Cutter подходят площадки большого размера.```",
        colour=0x2F3136)
    embed.add_field(
        name="СБОРКИ",
        value=# Автор Artificial Intelligence
              "• [«Боевой» шахтер на 512 тонн груза](https://s.orbis.zone/cdy2)\n"
              "• [«Боевой» грузовик на 720 тонн груза](https://s.orbis.zone/cdy6)\n"
              "• [AX под комбат зоны](https://s.orbis.zone/ce3k)\n"
              "• Автор: <@232550259841171466>\n\n"
              
              # Автор HarrisonSould
              "• [Кутер для PVE](https://s.orbis.zone/6j86)\n"
              "• [Cutter Исследователь](https://s.orbis.zone/3uwe)\n"
              "• [Cutter для AFK фарма](https://s.orbis.zone/3u9s)\n"
              "• [Каттер Майнер 3.3](https://s.orbis.zone/2z1u)\n"
              "• [Майнер LTD](https://s.orbis.zone/6j85)\n"
              "• Автор: <@270156067055468544>\n\n"
              
              # Автор I-RevolveR-I
              "• [Cutter AX](https://s.orbis.zone/3uwb)\n"
              "• Автор: I-RevolveR-I\n\n"
              
              "• [Каттер торговец](https://s.orbis.zone/4_bl)\n"
              "• Автор: <@344735291384528898>\n\n"
              
              "• [GOLD RUSH Майнер](https://s.orbis.zone/5rbv)\n"
              "• Автор: <@402878540917374976>")
    embed.set_image(url='attachment://gutamaya-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Imperial Cutter // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Type-7 Transporter
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="type7", description="Список сборок для «Type-7 Transporter»")
async def mamba(ctx):
    file = discord.File("sources\images\corporations\lakon-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title='Type-7 Transporter',
        url='https://elite-dangerous.fandom.com/wiki/Type-7_Transporter',
        description='```Type-7 Transporter — это грузовой корабль, представляющий собой средний вариант между небольшим «Type-6 Transporter» и крупным «Type-9 Heavy». Выдающаяся дальность прыжка и сравнительно низкая цена делают данную модель привлекательной для тех, кто хочет построить карьеру в торговле.```',
        colour=0x2F3136)
    embed.add_field(
        name='СБОРКИ',
        value=# Автор HarrisonSould
              '• [Type-7 Taxi](https://s.orbis.zone/3z3d)\n'
              '• [T7 Майнер Алмазов](https://s.orbis.zone/6v90)\n'
              '• [Т7 исследователь](https://s.orbis.zone/3qk-)\n'
              '• Автор: <@270156067055468544>')
    embed.set_image(url='attachment://lakon-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Type-7 Transporter // КОНЕЦ


# region •••••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Type-9 Heavy
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="type9", description="Список сборок для «Type-9 Heavy»")
async def mamba(ctx):
    file = discord.File("sources\images\corporations\lakon-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title='Type-9 Heavy',
        url='https://elite-dangerous.fandom.com/wiki/Type-9_Heavy',
        description='```Type-9 Heavy — это один из самых больших грузовых кораблей на рынке. И хотя по грузоподъёмности он уступает Imperial Cutter, Type-9 стоит значительно дешевле, а для его приобретения не требуется звание Имперского флота. Кроме того, благодаря возможности установки отсека для истребителя, данная модель популярна среди торговцев, которым важно защитить свой груз от воров. Для Type-9 Heavy подходят посадочные площадки большого размера.```',
        colour=0x2F3136)
    embed.add_field(
        name='СБОРКИ',
        value=# Автор Artificial Intelligence
              '• [Защищенный грузовик](https://s.orbis.zone/cdyb)\n'
              '• Автор: <@232550259841171466>\n\n'
              
              # Автор HarrisonSould
              '• [Майнер пейнита](https://s.orbis.zone/47u0)\n'
              '• [Грузовой](https://s.orbis.zone/3q_a)\n'
              '• [Miner 3.3](https://s.orbis.zone/3q_d)\n'
              '• Автор: <@270156067055468544>')
    embed.set_image(url='attachment://lakon-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# endregion ••••••••••••• КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Type-9 Heavy // КОНЕЦ


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Type-10 Defender
@ships.command(guild_ids=guild_ids_for_slash(), default_permission=False, name="type10", description="Список сборок для «Type-10 Defender»")
async def mamba(ctx):
    file = discord.File("sources\images\corporations\lakon-horizon.png")
    # region • Создаём сообщение
    embed = discord.Embed(
        title='Type-10 Defender',
        url='https://elite-dangerous.fandom.com/wiki/Type-9_Heavy',
        description='```Альянс поручил Lakon Spaceways изготовить универсальный Type-10 Defender, и для его создания компании пришлось полностью пересмотреть концепцию Type-9. Получившееся судно превзошло Type-9 в скорости, ускорении и манёвренности, а также может похвастаться более удачным расположением гнёзд. Корабль с подобными характеристиками изначально задумывался как боевое судно, однако благодаря вместительному грузовому отсеку он в равной степени подходит и торговцам. Для Type-10 Defender подходят посадочные платформы большого размера.```',
        colour=0x2F3136)
    embed.add_field(
        name='СБОРКИ',
        value=# Автор HarrisonSould
              "• [PVE T10](https://s.orbis.zone/3q_j)\n"
              "• [T10 с ракетами и многостволками](https://s.orbis.zone/3jt5)\n"
              "• [T10 Майнер Пейнита](https://s.orbis.zone/3uxv)\n"
              "• Автор: <@270156067055468544>\n\n"
              
              # Автор Klemyr
              "• [T10 Майнер 3.3 (Защищенный)](https://s.orbis.zone/2hq7)\n"
              "• Автор: <@189334900405436416>\n\n"
              
              # Автор Paffoc
              "• [Т10 Fuel Rat's](https://s.orbis.zone/3nc8)\n"
              "• Автор: Paffoc\n\n"
              
              # Автор ZLUKA
              "• [PVE T10 - Мародер](https://s.orbis.zone/3ukx)\n"
              "• Автор: ZLUKA\n\n"
              
              # Автор HolyFire
              "• [Т10 афк двухпоточник](https://s.orbis.zone/7r7a)\n"
              "• [Т10 афк призма](https://s.orbis.zone/7r7b)\n"
              "• Автор: HolyFire")
    embed.set_image(url='attachment://lakon-horizon.png')
    # endregion
    # Отправляем скрытое сообщение
    await ctx.respond(file=file, embed=embed, view=Button_group_for_ships(), ephemeral=True)


# ------------- КОМАНДА ОТОБРАЖЕНИЯ СБОРОК Type-10 Defender // КОНЕЦ


client.run(config.token)


# •••••• 🦆 •••••• СОЗДАЁМ ПРИЛОЖЕНИЕ И НАЗЫВАЕМ ЕГО CLIENT  // КОНЕЦ
