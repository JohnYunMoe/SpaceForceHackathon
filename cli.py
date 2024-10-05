import api as sfapi
import json

from rich.text import Text
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich_menu import Menu
from rich.prompt import Confirm



class CLI:
    def __init__(self):
        self.console = Console()
        self.username = ""
        self.password = ""
        self.api = sfapi.SpaceForceAPI()

    def login(self):
        self.console.clear()
        self.username = Prompt.ask("Enter username")
        self.password = Prompt.ask("Enter password", password=True)
        self.api.setUsernamePassword(self.username, self.password)
        #self.api.postSetLoginOAuthTokens(self.username, self.password)
        #self.api.getLoginStatus()

        self.mainmenu()
        

    def viewSatelliteList(self, offset=None, limit=None):
        self.console.clear()
        if(self.username != ""):
            usePrivate = Confirm.ask("Use private satellites?")
        else:
            usePrivate = False

        if(offset == None):
            offset = Prompt.ask("Enter offset", default=0)
            limit = Prompt.ask("Enter satellites per page", default=20)
        
        table = Table(title="Satellite List")

        if(usePrivate):
           satelliteList = self.api.getPrivateSatelliteList(offset=offset, limit=limit)
        else:
            satelliteList = self.api.getPublicSatelliteList(offset=offset, limit=limit)


        firstTime = False
        colors = ["red", "green", "blue", "yellow", "magenta", "cyan", "white"]
        satelliteList = json.loads(satelliteList)
        for satellite in satelliteList:
            if(not firstTime):
                for count, key in enumerate(satellite.keys()):
                    table.add_column(key, justify="center", style=colors[count % len(colors)])
                firstTime = True
        
            table.add_row(*[str(value) for value in satellite.values()])
            
        self.console.clear()
        self.console.print(table)
        option = Prompt.ask("View additional page, or return to main menu?", choices=["next", "previous", "main menu"])
        if(option == "next"):
            self.viewSatelliteList(offset=offset+limit, limit=limit)
        elif(option == "previous"):
            if(offset-limit < 0):
                self.viewSatelliteList(offset=0, limit=limit)
            else:
                self.viewSatelliteList(offset=offset-limit, limit=limit)
        elif(option == "main menu"):
            self.mainmenu()


    def mainmenu(self):
        self.console.clear()
        self.console.print("[bold]Code & Construct SpaceForce TUI[/bold]")
        options = [
            "login: enter credentials to login",
            "view satellite list: view a list of satellites",
            "search satellites: search for satellites",
            "search by NORAD ID: search for a satellite by NORAD ID",
        ]
        if(self.username != ""):
            options.append("logout: logout of the API")

        self.console.print("\n")
        title = Text("? Select option to continue:", style="bold")
        title.stylize("bold yellow", 0, 1)

        menu = Menu(
            *options,
            color="cyan",
            title=title,
            align="left",
            rule=False,
            panel=False,
            selection_char=">",
            highlight_color="cyan",
        )
        selected = menu.ask(screen=False)

        if selected == "login: enter credentials to login":
            self.login()
        elif selected == "view satellite list: view a list of satellites":
            self.viewSatelliteList()
 


if __name__ == "__main__":
    CLI().mainmenu()
