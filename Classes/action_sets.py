from Actions.find_and_click_image_action import action_class
from Actions.find_and_click_image_action import action_classMouse
from Actions.press_key_action import PressKeyAction
from Actions.find_image_action import FindImageAction
from Actions.manual_click_action import ManualClickAction
from Actions.manual_sleep_action import ManualSleepAction
from Actions.quit_action import QuitAction
from Actions.lyceum_action import LyceumAction
from Actions.extract_text_action import ExtractTextAction
from Actions.find_marauder_action import FindMarauderAction
from Actions.screenshot_action import ScreenshotAction
from Actions.chatgpt_action import ChatGPTAction
from Actions.wait_for_keypress_action import WaitForKeyPressAction
from state_machine import StateMachine
from Actions.find_gems_action import FindGemAction
from helpers import Helpers
import random
import inspect
import time


class ActionSets:
    def __init__(self, OS_ROKBOT):
        self.OS_ROKBOT = OS_ROKBOT
    
    def create_machine(self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        return StateMachine()

    def get_action_class(self, move_mouse_checked):
        """Возвращает класс действия в зависимости от состояния флажка move_mouse."""
        if move_mouse_checked:
            return FindAndClickImageActionMouse
        else:
            return FindAndClickImageAction

    def TEST2(self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)


        machine = self.create_machine()
        machine.add_state("1", action_class('Media/escxdark.png', delay=random.uniform(2, 5)), "2", "2")
        machine.add_state("2", action_class('Media/escxwhite.png', delay=random.uniform(2, 5)), "1", "1")
        machine.set_initial_state("1")
        return machine

    def run_random(self):
        scripts = [
            method
            for method_name, method in inspect.getmembers(self, predicate=inspect.ismethod)
            if method.__self__ == self
            and not method_name.startswith('_')
            and method_name not in ('__init__', 'create_machine', 'run_random', 'TEST', 'get_action_class')
        ]
    
        while True:
            if self.OS_ROKBOT.stop_event.is_set():
                self.OS_ROKBOT.stop_event.clear()
                return
    
            script = random.choice(scripts)
            if script.__name__ == "help_ally":
                run_time = random.randint(40, 60)  
        #    elif script.__name__ == "figwam":
        #       run_time = random.randint(30, 50)
            else:
                run_time = random.randint(60, 300) 
    
            start_time = time.time()
            message = f"Running script: {script.__name__} for {run_time} seconds"
            self.OS_ROKBOT.UI.currentState(message)
            print(message)  # Вывод в консоль
    
            machine = script()
            while time.time() - start_time < run_time:
                if self.OS_ROKBOT.stop_event.is_set():
                    self.OS_ROKBOT.stop_event.clear()
                    return    
                if machine.current_state:
                    machine.execute()
                    time.sleep(1)  # Добавим задержку, чтобы не перегружать систему
                else:
                    break
    
            message = f"Script {script.__name__} completed"
            self.OS_ROKBOT.UI.currentState(message)
            print(message)  # Вывод в консоль

    def TEST (self, move_mouse_checked):
        machine = self.create_machine()
        machine.add_state("1", action_classMouse('Media/escxdark.png', delay=random.uniform(2, 5)), "2", "2")
        machine.add_state("2", action_class('Media/escxwhite.png', delay=random.uniform(2, 5)), "1", "1")
        machine.set_initial_state("1")
        return machine


    def scout_karta(self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        
        machine = self.create_machine()
        machine.add_state("1q", FindImageAction('Media/explorehome.png', delay=random.uniform(1, 2)), "1w", "1")
        machine.add_state("1w", action_class('Media/explorehome.png', delay=random.uniform(2, 5)), "1", "restart")

        machine.add_state("1", action_class('Media/explorenight.png', delay=random.uniform(2, 5), offset_y=60), "2", "4q")
        machine.add_state("2", action_class('Media/exploreicon.png', delay=random.uniform(2, 5)), "3", "restart")
        machine.add_state("3", action_class('Media/exploreaction.png', delay=random.uniform(2, 5)), "5", "4")
        machine.add_state("4", action_class('Media/exploreaction3.png', delay=random.uniform(2, 5)), "5", "4q")
        machine.add_state("5", action_class('Media/exploreaction2.png', delay=random.uniform(2, 5)), "6", "4")
        machine.add_state("6", action_class('Media/sendaction.png', delay=random.uniform(2, 5)), "7", "5")

        machine.add_state("4q", FindImageAction('Media/exploreaction4.png', delay=random.uniform(1, 2)), "4w", "4w")
        machine.add_state("4w", action_class('Media/exploreaction5.png', delay=random.uniform(2, 5)), "2", "restart")

        machine.add_state("restart", action_class('Media/explorehome.png', delay=random.uniform(2, 5)), "1q", "restart1")
        machine.add_state("restart1", FindImageAction('Media/explorehome2.png', delay=random.uniform(1, 2)), "1q", "restart2")
        machine.add_state("restart2", PressKeyAction('escape', delay=random.uniform(1, 2)), "restart3")
        machine.add_state("restart3", action_class('Media/otmena.png', delay=random.uniform(2, 5)), "1q", "1q")

        machine.add_state("7", action_class('Media/explorehome.png', delay=random.uniform(2, 5)), "1q", "restart")

        machine.set_initial_state("1q")
        return machine

    def farm_varvar_heal(self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()

        machine.add_state("1q", FindImageAction('Media/explorehome.png', delay=random.uniform(1, 2)), "1", "1w")
        machine.add_state("1w", FindImageAction('Media/explorehome2.png', delay=random.uniform(1, 2)), "1e", "restart")
        machine.add_state("1e", action_class('Media/pickuptroopscured.png', delay=random.uniform(2, 5)), "1", "1r")
        machine.add_state("1r", action_class('Media/curetroops.png', delay=random.uniform(2, 5)), "1e", "1r")
        machine.add_state("1r", action_class('Media/explorehome2.png', delay=random.uniform(2, 5)), "1", "restart")

        machine.add_state("1", action_class('Media/ficon.png', delay=random.uniform(2, 5)), "2", "restart")
        machine.add_state("2", action_class('Media/barbland.png', delay=random.uniform(2, 5)), "3", "restart")
        machine.add_state("3", action_class('Media/searchaction.png', delay=random.uniform(2, 5)), "4", "restart")
        machine.add_state("4", action_class('Media/arrow.png', delay=1.5, offset_y=105), "5", "restart")
        machine.add_state("5", action_class('Media/attackaction.png', delay=random.uniform(2, 5)), "6", "restart")
        machine.add_state("6", action_class('Media/newtroopaction.png', delay=random.uniform(2, 5)), "7", "restart")
        machine.add_state("7", action_class('Media/marchaction.png', delay=random.uniform(2, 5)), "alliancehelp", "restart")
        machine.add_state("alliancehelp", action_class('Media/alliancehelp.png', delay=random.uniform(2, 5)), "proverka1", "proverka1")
        machine.add_state("proverka1", FindImageAction('Media/proverka1.png', delay=random.uniform(1, 2)), "proverka1", "heal1")

        machine.add_state("heal1", FindImageAction('Media/explorehome.png', delay=random.uniform(1, 2)), "home", "explorehome2")
        machine.add_state("home", action_class('Media/explorehome.png', delay=random.uniform(2, 5)), "explorehome2", "restart")
        machine.add_state("explorehome2", FindImageAction('Media/explorehome2.png', delay=random.uniform(1, 2)), "curetroops", "restart")
        machine.add_state("curetroops", action_class('Media/curetroops.png', delay=random.uniform(2, 5)), "healaction", "restart")
        machine.add_state("healaction", action_class('Media/healaction.png', delay=random.uniform(2, 5)), "pickuptroopscured", "restart")
        machine.add_state("pickuptroopscured", action_class('Media/pickuptroopscured.png', delay=random.uniform(2, 5)), "1q", "restart")

        machine.add_state("restart", action_class('Media/explorehome.png', delay=random.uniform(2, 5)), "1q", "restart1")
        machine.add_state("restart1", FindImageAction('Media/explorehome2.png', delay=random.uniform(1, 2)), "1q", "restart2")
        machine.add_state("restart2", PressKeyAction('escape', delay=random.uniform(1, 2)), "restart3")
        machine.add_state("restart3", action_class('Media/otmena.png', delay=random.uniform(2, 5)), "1q", "1q")

        machine.set_initial_state("1q")
        return machine
    
    def help_ally (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("alliancehelp", FindImageAction('Media/alliancehelp.png'), "alliancehelp2", "explorehome")
        machine.add_state("alliancehelp2", action_class('Media/alliancehelp.png', delay=random.uniform(2, 5)), "explorehome", "explorehome")
        machine.add_state("explorehome", FindImageAction('Media/explorehome.png'), "explorehome2", "corn")
        machine.add_state("explorehome2", action_class('Media/explorehome.png', delay=random.uniform(2, 5)), "corn", "corn")

        machine.add_state("corn", FindImageAction('Media/corn.png'), "corn2", "wood")
        machine.add_state("corn2", action_class('Media/corn.png', delay=random.uniform(2, 5)), "wood", "wood")
        machine.add_state("wood", FindImageAction('Media/wood.png'), "wood2", "gold")
        machine.add_state("wood2", action_class('Media/wood.png', delay=random.uniform(2, 5)), "gold", "gold")
        machine.add_state("gold", FindImageAction('Media/gold.png'), "gold2", "stone")
        machine.add_state("gold2", action_class('Media/gold.png', delay=random.uniform(2, 5)), "stone", "stone")
        machine.add_state("stone", FindImageAction('Media/stone.png'), "stone2", "curetroops")
        machine.add_state("stone2", action_class('Media/stone.png', delay=random.uniform(2, 5)), "curetroops", "curetroops")
        
        machine.add_state("curetroops", FindImageAction('Media/curetroops.png'), "curetroops2", "pickuptroopscured1")
        machine.add_state("curetroops2", action_class('Media/curetroops.png', delay=random.uniform(2, 5)), "healaction", "restart")
        machine.add_state("healaction", action_class('Media/healaction.png', delay=random.uniform(2, 5)), "pickuptroopscured", "restart")
        machine.add_state("pickuptroopscured1", FindImageAction('Media/pickuptroopscured.png'), "pickuptroopscured", "restart")
        machine.add_state("pickuptroopscured", action_class('Media/pickuptroopscured.png', delay=random.uniform(10, 15)), "alliancehelp", "restart")

        machine.add_state("restart", FindImageAction('Media/explorehome.png'), "restart11", "restart1")
        machine.add_state("restart11", action_class('Media/explorehome.png', delay=random.uniform(2, 5)), "alliancehelp", "restart1")
        
        machine.add_state("restart1", FindImageAction('Media/explorehome2.png'), "alliancehelp", "restart211")
        machine.add_state("restart211", FindImageAction('Media/escxdark.png'), "restart21", "restart222")
        machine.add_state("restart21", action_class('Media/escxdark.png', delay=random.uniform(2, 5)), "alliancehelp", "restart22")
        machine.add_state("restart222", FindImageAction('Media/escxwhite.png'), "restart22", "restart2")
        machine.add_state("restart22", action_class('Media/escxwhite.png', delay=random.uniform(2, 5)), "alliancehelp", "restart2")

        machine.add_state("restart2", PressKeyAction('escape', delay=random.uniform(1, 2)), "restart33")
        machine.add_state("restart33", FindImageAction('Media/otmena.png'), "restart3", "alliancehelp")
        machine.add_state("restart3", action_class('Media/otmena.png', delay=random.uniform(2, 5)), "alliancehelp", "alliancehelp")
        machine.set_initial_state("alliancehelp")
        return machine
        
    def _scout_explore(self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("explorenight", action_class('Media/explorenight.png',delay=.4, offset_y=60), "openmsgs", "exploreday")
        
        machine.add_state("exploreday", action_class('Media/explore.png', delay=1, offset_y=60), "openmsgs", "explorenight")

        machine.add_state("openmsgs", PressKeyAction('z'), "reportactive")
        machine.add_state("reportactive", ManualClickAction(27,8,delay=.2), "explorationreport")
        machine.add_state("explorationreport", action_class('Media/explorationreport.png',delay=.2), "villagereport", "explorationreportactive")
        machine.add_state("explorationreportactive", action_class('Media/explorationreportactive.png',delay=.2), "villagereport", "explorationreport")

        machine.add_state("villagereport", action_class('Media/villagereport.png', offset_x=370,delay=0), "checkexploredvillage", "barbreport")
        machine.add_state("checkexploredvillage", action_class('Media/reportbanner.png', delay=0), "barbreport", "clickmonument")

        machine.add_state("barbreport", action_class('Media/barbreport.png', offset_x=370,delay=0), "checkexploredbarb", "barbreport2")
        machine.add_state("checkexploredbarb", action_class('Media/reportbanner.png', delay=0), "barbreport2", "clickmonument")

        machine.add_state("barbreport2", action_class('Media/barbreport2.png', offset_x=370,delay=0), "checkexploredbarb2", "passreport")
        machine.add_state("checkexploredbarb2", action_class('Media/reportbanner.png', delay=0), "passreport", "clickmonument")
        
        machine.add_state("passreport", action_class('Media/passreport.png', offset_x=370,delay=0), "checkexploredpass", "holyreport")
        machine.add_state("checkexploredpass", action_class('Media/reportbanner.png', delay=0), "holyreport", "clickmonument")

        machine.add_state("holyreport", action_class('Media/holyreport.png', offset_x=370,delay=0), "checkexploredholy", "cavereport")
        machine.add_state("checkexploredholy", action_class('Media/reportbanner.png', delay=0), "cavereport", "clickmonument")

        machine.add_state("cavereport", action_class('Media/cavereport.png', offset_x=300, offset_y=20,delay=.1), "checkexploredcave", "emptyreport")
        machine.add_state("checkexploredcave", action_class('Media/reportbanner.png', delay=.1), "emptyreport", "clickcave")
        machine.add_state("clickcave", ManualClickAction(50,54,delay=2), "investigateaction")
        machine.add_state("investigateaction", action_class('Media/investigateaction.png',delay=.2), "sendactioncave","investigateaction")
        machine.add_state("sendactioncave", action_class('Media/sendaction.png',delay=.2), "backtocity","sendactioncave")



        machine.add_state("checkexplored", action_class('Media/reportbanner.png', delay=.1), "scouticon", "clickmonument")
        machine.add_state("scouticon", action_class('Media/scoutticon.png', offset_x=30,delay=.1), "barbreport", "failexplorenight")
        machine.add_state("clickmonument", ManualClickAction(50,54,delay=2), "backtocitylong", "clickmonument")
        machine.add_state("backtocitylong", PressKeyAction('space',delay=4), "explorenight")
        # same but press esc

        machine.add_state("emptyreport", PressKeyAction('escape'), "failexplorenight")
        machine.add_state("failexplorenight", action_class('Media/explorenight.png', offset_y=25), "exploreicon", "failexploreday")
        machine.add_state("failexploreday", action_class('Media/explore.png', offset_y=25), "exploreicon", "failexplorenight")

        machine.add_state("exploreicon", action_class('Media/exploreicon.png',delay=.4), "exploreaction", "failexplorenight")
        machine.add_state("exploreaction", action_class('Media/exploreaction.png',delay=1), "exploreactionfog", "exploreaction")

        machine.add_state("exploreactionfog", action_class('Media/exploreaction.png',delay=2), "exploreactionfogcheck", "exploreactionfogcheck")
        machine.add_state("exploreactionfogcheck", action_class('Media/exploreaction.png',delay=.1), "exploreactionfog", "sendaction")

        machine.add_state("sendaction", action_class('Media/sendaction.png',delay=1.2, retard=1), "sendactioncheck", "sendactioncheck")
        machine.add_state("sendactioncheck", action_class('Media/sendaction.png',delay=1.2, retard=1), "sendaction", "backtocity")

        machine.add_state("backtocity", PressKeyAction('space'),"explorenight")
        machine.set_initial_state("explorenight")
        return machine
        
    def _farm_varvars (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("1q", FindImageAction('Media/explorehome.png', random.uniform(1, 2)), "1","1w")
        machine.add_state("1w", FindImageAction('Media/explorehome2.png', random.uniform(1, 2)), "1e","restart")
        machine.add_state("1e", action_class('Media/explorehome2.png', random.uniform(2, 5)), "1", "restart")

        machine.add_state("1", action_class('Media/ficon.png',random.uniform(2, 5)), "2", "restart")
        machine.add_state("2", action_class('Media/barbland.png',random.uniform(2, 5)), "3", "restart")
        machine.add_state("3", action_class('Media/searchaction.png',random.uniform(2, 5)), "4", "restart")
        machine.add_state("4", action_class('Media/arrow.png',random.uniform(2, 5), offset_y=105), "5","restart")
        machine.add_state("5", action_class('Media/attackaction.png',random.uniform(2, 5)), "6", "restart")
        machine.add_state("6", action_class('Media/newtroopaction.png',random.uniform(2, 5)), "7", "restart")
        machine.add_state("7", action_class('Media/marchaction.png',random.uniform(2, 15)), "10", "restart")
        #machine.add_state("8", FindImageAction('Media/victory2.png', delay=1), "10","8")
        #machine.add_state("9", FindImageAction('Media/victoryreturn.png', delay=1), "10","9")
        machine.add_state("10", ManualSleepAction(delay=60), "1q", "restart") # Ожидание 1 минуту

        machine.add_state("restart", action_class('Media/explorehome.png', random.uniform(2, 5)), "1q", "restart1")
        machine.add_state("restart1", FindImageAction('Media/explorehome2.png', random.uniform(1, 3)), "1q", "restart2")
        machine.add_state("restart2", PressKeyAction('escape', random.uniform(1, 3)), "restart3")
        machine.add_state("restart3", action_class('Media/otmena.png', delay=random.uniform(2, 5)), "1q", "1q")

        machine.set_initial_state("1q")
        return machine
        
    def _farm_barb_all (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("restart", PressKeyAction('escape'), "cityview")
        machine.add_state("cityview", PressKeyAction('space',delay=.3), "birdview","cityview")
        machine.add_state("birdview", PressKeyAction('f',delay=.3), "barbland","cityview")
        machine.add_state("barbland", action_class('Media/barbland.png',delay=.3), "searchaction","restart")
        machine.add_state("searchaction", action_class('Media/searchaction.png'), "arrow","restart")
        machine.add_state("arrow", action_class('Media/arrow.png',delay=1.5, offset_y=105), "attackaction","restart")
        machine.add_state("attackaction", action_class('Media/attackaction.png',delay=.3), "lohar","restart")
        machine.add_state("lohar", ManualClickAction(96,80), "smallmarchaction","newtroopaction")
        
        machine.add_state("newtroopaction", action_class('Media/newtroopaction.png',delay=.3), "marchaction","restart")
        machine.add_state("marchaction", action_class('Media/marchaction.png'), "victory","restart")

        #machine.add_state("lohar", ManualClickAction(96,80), "smallmarchaction","newtroopaction")
        
        #machine.add_state("lohar", action_class('Media/lohar.png'), "smallmarchaction","newtroopaction")
        #machine.add_state("newtroopaction", action_class('Media/newtroopaction.png'), "marchaction","newtroopaction")
        #machine.add_state("marchaction", action_class('Media/marchaction.png'), "victory","marchaction")
        machine.add_state("smallmarchaction", action_class('Media/smallmarchaction.png',delay=.5), "victory","restart")
        machine.add_state("victory", FindImageAction('Media/victory.png', delay=2), "birdview","victory")
        machine.set_initial_state("cityview")
        return machine
    
    def _train_troops (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("restart", PressKeyAction('escape'), "stable")
        machine.add_state("stable", action_class('Media/stable.png', offset_x=10), "speedupicon","restart")
        machine.add_state("speedupicon", action_class('Media/speedupicon.png'), "use","trainhorse")
        machine.add_state("use", ManualClickAction(65,40), "mult","stable")
        machine.add_state("mult", action_class('Media/mult.png'), "use2","stable")
        machine.add_state("use2", ManualClickAction(65,40), "leavemult","stable")
        machine.add_state("leavemult", PressKeyAction('escape'), "stable","stable")

        machine.add_state("trainhorse", action_class('Media/trainhorse.png'), "t1cav","stable")
        machine.add_state("t1cav", action_class('Media/t1cav.png'), "upgrade","stable")
        machine.add_state("upgrade", action_class('Media/upgrade.png'), "upgradeaction","stable")
        machine.add_state("upgradeaction", action_class('Media/upgradeaction.png'), "trainbutton","stable")
        machine.add_state("trainbutton", action_class('Media/trainbutton.png'), "stable","stable")
        machine.set_initial_state("stable")
        return machine
    
    def _farm_rss (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        
        machine.add_state("pause", PressKeyAction('escape', retard=65), "restart")
        machine.add_state("restart", PressKeyAction('escape'), "checkesc")
        machine.add_state("checkesc", action_class('Media/escx.png'), "cityview","cityview",)
        machine.add_state("cityview", PressKeyAction('space'), "birdview")
        machine.add_state("birdview",action_class('Media/ficon.png'), Helpers.getRandomRss(),"restart")

        machine.add_state("logicon", action_class('Media/logicon.png'), "searchaction","restart")
        machine.add_state("cornicon", action_class('Media/cornicon.png'), "searchaction","restart")
        machine.add_state("goldicon", action_class('Media/goldicon.png'), "searchaction","restart")
        machine.add_state("stoneicon", action_class('Media/stoneicon.png'), "searchaction","restart")
        machine.add_state("searchaction", action_class('Media/searchaction.png'), "arrow","logicon")
        machine.add_state("arrow", ManualClickAction(x=50, y=50, delay=1.5), "gatheraction","restart")
        machine.add_state("gatheraction", action_class('Media/gatheraction.png'), "newtroopaction","restart")

        machine.add_state("newtroopaction", action_class('Media/newtroopaction.png', delay=1), "marchaction","smallmarchaction")
        machine.add_state("smallmarchaction", FindImageAction('Media/smallmarchaction.png'), "pause","restart")


        machine.add_state("marchaction", action_class('Media/marchaction.png'), "birdview","restart")

        machine.set_initial_state("cityview")
        return machine
    
    def _farm_rss_new (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("pause1",  ManualSleepAction(delay=10), "test")
        machine.add_state("test",  ScreenshotAction(96,98,18.6,20.4,delay=1), "test2")
        machine.add_state("test2", ExtractTextAction(description= "marchcount"), "birdview","pause1")
        machine.add_state("pause", PressKeyAction('escape', retard=.5), "pause1")
        machine.add_state("restart", PressKeyAction('escape'), "checkesc")
        machine.add_state("checkesc", action_class('Media/escx.png'), "cityview","cityview",)
        machine.add_state("cityview", PressKeyAction('space'), "birdview")
        machine.add_state("birdview",action_class('Media/ficon.png'), Helpers.getRandomRss(),"restart")

        machine.add_state("logicon", action_class('Media/logicon.png'), "searchaction","restart")
        machine.add_state("cornicon", action_class('Media/cornicon.png'), "searchaction","restart")
        machine.add_state("goldicon", action_class('Media/goldicon.png'), "searchaction","restart")
        machine.add_state("stoneicon", action_class('Media/stoneicon.png'), "searchaction","restart")
        machine.add_state("searchaction", action_class('Media/searchaction.png'), "arrow","logicon")
        machine.add_state("arrow", ManualClickAction(x=50, y=50, delay=1.5), "gatheraction","restart")
        machine.add_state("gatheraction", action_class('Media/gatheraction.png'), "newtroopaction","restart")

        machine.add_state("newtroopaction", action_class('Media/newtroopaction.png', delay=1), "marchaction","smallmarchaction")
        machine.add_state("smallmarchaction", FindImageAction('Media/smallmarchaction.png'), "pause","restart")


        machine.add_state("marchaction", action_class('Media/marchaction.png'), "test","restart")

        machine.set_initial_state("test")
        return machine
    
    def _farm_gems (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        #machine.add_state("0", PressKeyAction('space',retard=4), "1")
        #machine.add_state("1", PressKeyAction('space'), "2")
        machine.add_state("2",FindGemAction(),"3")

        machine.set_initial_state("2")
        return machine
    
    def _loharjr (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("0", PressKeyAction('space',retard=4), "1")
        machine.add_state("1", PressKeyAction('space'), "2")
        machine.add_state("2",FindMarauderAction(),"3")
        machine.add_state("3", action_class('Media/attackaction.png',delay=.3), "4","0")
        machine.add_state("4", action_class('Media/newtroopaction.png',delay=.3), "5","5f")
        machine.add_state("5f", ManualClickAction(96,80), "6f")
        machine.add_state("6f", action_class('Media/smallmarchaction.png'), "7","0")
        machine.add_state("5", ManualClickAction(75,78), "6")
        machine.add_state("6", action_class('Media/marchaction.png'), "7","0")

        machine.add_state("7", PressKeyAction('escape'), "8")
        machine.add_state("8", action_class('Media/applus.png'), "9","0")
        machine.add_state("9", action_class('Media/apuse.png'), "10","0")
        machine.add_state("10", ManualClickAction(60,40), "11","11")
        machine.add_state("11", PressKeyAction('escape'), "12")
        machine.add_state("12", PressKeyAction('escape'), "13")
        machine.add_state("13", FindImageAction('Media/victory.png', delay=2), "14","13")
        machine.add_state("14", FindImageAction('Media/defeat.png', delay=0), "15","2")
        machine.add_state("15", FindImageAction('Media/armyc.png', delay=5), "15","0")
        #machine.add_state("14", ExtractTextAction(description= "marchcount"), "0","2")
        #machine.add_state("13", FindImageAction('Media/armyc.png', delay=5), "13","2")
        #
        #machine.add_state("other", PressKeyAction('left'), "marchaction")
       # machine.add_state("other", action_class('Media/marauder.png', delay=1), "marchaction","inventory")



        machine.set_initial_state("1")
        return machine

    def _loharjrt (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        
        machine.add_state("inventory", PressKeyAction('i'), "other")
        machine.add_state("other", ManualClickAction(x=80, y=20), "loharjr","inventory")
        machine.add_state("loharjr", action_class('Media/loharjr.png'), "useaction","inventory")
        machine.add_state("useaction", action_class('Media/useaction.png'), "arrow","inventory")
        machine.add_state("arrow", action_class('Media/arrow.png',delay=1.5, offset_y=105), "rallyaction","inventory")
        machine.add_state("rallyaction", action_class('Media/rallyaction.png',delay=.3), "rallysmallaction","inventory")
        machine.add_state("rallysmallaction", action_class('Media/rallysmallaction.png',delay=.5), "marchaction","inventory")
        machine.add_state("marchaction", action_class('Media/marchaction.png',delay=.5), "end","inventory")
        machine.add_state("end", QuitAction(OS_ROKBOT=self.OS_ROKBOT), "inventory","inventory")


        machine.set_initial_state("inventory")
        return machine
    
    def _farm_wood (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("pause1",  ManualSleepAction(delay=10), "test")
        machine.add_state("test",  ScreenshotAction(96,98,18.6,20.4), "test2")
        machine.add_state("test2", ExtractTextAction(description= "marchcount"), "restart","pause1")
        machine.add_state("pause", PressKeyAction('escape', retard=.5), "pause1")
        machine.add_state("restart", PressKeyAction('escape'), "checkesc")
        machine.add_state("checkesc", action_class('Media/escx.png'), "cityview","cityview",)
        machine.add_state("cityview", PressKeyAction('space'), "birdview")
        machine.add_state("birdview",action_class('Media/ficon.png'), "logicon","restart")

        machine.add_state("logicon", action_class('Media/logicon.png'), "searchaction","restart")
        machine.add_state("searchaction", action_class('Media/searchaction.png'), "arrow","logicon")
        machine.add_state("arrow", ManualClickAction(x=50, y=50, delay=1.5), "gatheraction","restart")
        machine.add_state("gatheraction", action_class('Media/gatheraction.png'), "newtroopaction","restart")

        machine.add_state("newtroopaction", action_class('Media/newtroopaction.png', delay=1), "marchaction","smallmarchaction")
        machine.add_state("smallmarchaction", FindImageAction('Media/smallmarchaction.png'), "pause","restart")


        machine.add_state("marchaction", action_class('Media/marchaction.png'), "test","restart")

        machine.set_initial_state("test")
        return machine
    
    def _farm_food (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("pause1",  ManualSleepAction(delay=10), "test")
        machine.add_state("test",  ScreenshotAction(96,98,18.6,20.4), "test2")
        machine.add_state("test2", ExtractTextAction(description= "marchcount"), "restart","pause1")
        machine.add_state("pause", PressKeyAction('escape', retard=.5), "pause1")
        machine.add_state("restart", PressKeyAction('escape'), "checkesc")
        machine.add_state("checkesc", action_class('Media/escx.png'), "cityview","cityview",)
        machine.add_state("cityview", PressKeyAction('space'), "birdview")
        machine.add_state("birdview",action_class('Media/ficon.png'), "cornicon","restart")

        machine.add_state("cornicon", action_class('Media/cornicon.png'), "searchaction","restart")
        machine.add_state("searchaction", action_class('Media/searchaction.png'), "arrow","cornicon")
        machine.add_state("arrow", ManualClickAction(x=50, y=50, delay=1.5), "gatheraction","restart")
        machine.add_state("gatheraction", action_class('Media/gatheraction.png'), "newtroopaction","restart")

        machine.add_state("newtroopaction", action_class('Media/newtroopaction.png', delay=1), "marchaction","smallmarchaction")
        machine.add_state("smallmarchaction", FindImageAction('Media/smallmarchaction.png'), "pause","restart")


        machine.add_state("marchaction", action_class('Media/marchaction.png'), "test","restart")

        machine.set_initial_state("test")
        return machine
    
    def _farm_stone (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("pause1",  ManualSleepAction(delay=10), "test")
        machine.add_state("test",  ScreenshotAction(96,98,18.6,20.4), "test2")
        machine.add_state("test2", ExtractTextAction(description= "marchcount"), "restart","pause1")
        machine.add_state("pause", PressKeyAction('escape', retard=.5), "pause1")
        machine.add_state("restart", PressKeyAction('escape'), "checkesc")
        machine.add_state("checkesc", action_class('Media/escx.png'), "cityview","cityview",)
        machine.add_state("cityview", PressKeyAction('space'), "birdview")
        machine.add_state("birdview",action_class('Media/ficon.png'), "stoneicon","restart")

        machine.add_state("stoneicon", action_class('Media/stoneicon.png'), "searchaction","restart")
        machine.add_state("searchaction", action_class('Media/searchaction.png'), "arrow","stoneicon")
        machine.add_state("arrow", ManualClickAction(x=50, y=50, delay=1.5), "gatheraction","restart")
        machine.add_state("gatheraction", action_class('Media/gatheraction.png'), "newtroopaction","restart")

        machine.add_state("newtroopaction", action_class('Media/newtroopaction.png', delay=1), "marchaction","smallmarchaction")
        machine.add_state("smallmarchaction", FindImageAction('Media/smallmarchaction.png'), "pause","restart")


        machine.add_state("marchaction", action_class('Media/marchaction.png'), "test","restart")

        machine.set_initial_state("test")
        return machine
    
    def _farm_gold (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("pause1",  ManualSleepAction(delay=10), "armyc")
        machine.add_state("armyc", FindImageAction('Media/armyc.png'), "test","pause1")
        machine.add_state("test",  ScreenshotAction(96,98,18.6,20.5), "test2")
        machine.add_state("test2", ExtractTextAction(description= "marchcount"), "restart","pause1")
        machine.add_state("pause", PressKeyAction('escape', retard=.5), "pause1")
        machine.add_state("restart", PressKeyAction('escape'), "checkesc")
        machine.add_state("checkesc", action_class('Media/escx.png'), "cityview","cityview",)
        machine.add_state("cityview", PressKeyAction('space'), "birdview")
        machine.add_state("birdview",action_class('Media/ficon.png'), "goldicon","restart")

        machine.add_state("goldicon", action_class('Media/goldicon.png'), "searchaction","restart")
        machine.add_state("searchaction", action_class('Media/searchaction.png'), "arrow","goldicon")
        machine.add_state("arrow", ManualClickAction(x=50, y=50, delay=1.5), "gatheraction","restart")
        machine.add_state("gatheraction", action_class('Media/gatheraction.png'), "newtroopaction","restart")

        machine.add_state("newtroopaction", action_class('Media/newtroopaction.png', delay=1), "marchaction","smallmarchaction")
        machine.add_state("smallmarchaction", FindImageAction('Media/smallmarchaction.png'), "pause","restart")


        machine.add_state("marchaction", action_class('Media/marchaction.png'), "armyc","restart")

        machine.set_initial_state("armyc")
        return machine

    def _lyceum (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("sstittle",  ScreenshotAction(33.7,77,33.5,43), "ettitle")
        machine.add_state("ettitle", ExtractTextAction(description= "Q"), "ssq1")
        machine.add_state("ssq1", ScreenshotAction(33,52,45,51), "eq1")
        machine.add_state("eq1",ExtractTextAction(description= "A"), "ssq2")
        machine.add_state("ssq2", ScreenshotAction(57,76,45,51), "eq2")
        machine.add_state("eq2", ExtractTextAction(description= "B"), "ssq3")
        machine.add_state("ssq3",  ScreenshotAction(33,54,54,60), "eq3")
        machine.add_state("eq3", ExtractTextAction(description= "C"), "ssq4")
        machine.add_state("ssq4", ScreenshotAction(57,76,54,60), "eq4")
        machine.add_state("eq4", ExtractTextAction(description= "D"), "lyceumManual")
        machine.add_state("lyceumManual", LyceumAction(retard=1.5),"sstittle","lyceumGPT")
        machine.add_state("lyceumGPT", ChatGPTAction(retard=1.5),"sstittle")
        machine.set_initial_state("sstittle")
        return machine
    
    def _lyceumMid (self, move_mouse_checked):
        action_class = self.get_action_class(move_mouse_checked)
        machine = self.create_machine()
        machine.add_state("keypress", WaitForKeyPressAction('k', "for the next question"), "sstittle","keypress")
        machine.add_state("sstittle",  ScreenshotAction(33.7,80,39.5,49), "ettitle")
        machine.add_state("ettitle", ExtractTextAction(description= "Q"), "ssq1")
        machine.add_state("ssq1", ScreenshotAction(33,52,49.5,57), "eq1")
        machine.add_state("eq1",ExtractTextAction(description= "A"), "ssq2")
        machine.add_state("ssq2", ScreenshotAction(57,74,49.5,57), "eq2")
        machine.add_state("eq2", ExtractTextAction(description= "B"), "ssq3")
        machine.add_state("ssq3",  ScreenshotAction(33,54,58,66), "eq3")
        machine.add_state("eq3", ExtractTextAction(description= "C"), "ssq4")
        machine.add_state("ssq4", ScreenshotAction(57,76,58,66), "eq4")
        machine.add_state("eq4", ExtractTextAction(description= "D"), "lyceumManual")
        machine.add_state("lyceumManual", LyceumAction(midterm=True,retard=1.5),"keypress","lyceumGPT")
        machine.add_state("lyceumGPT", ChatGPTAction(midterm=True,retard=1.5),"keypress")
        
        machine.set_initial_state("keypress")
        return machine