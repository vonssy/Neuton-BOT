import requests
import json
import urllib.parse
import os
from datetime import datetime
import time
from colorama import *
import pytz

wib = pytz.timezone('Asia/Jakarta')

class Neuton:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'neuton-tg-app-back.onrender.com',
            'Origin': 'https://neuton-tg-app-front.onrender.com',
            'Pragma': 'no-cache',
            'Referer': 'https://neuton-tg-app-front.onrender.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Neuton - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_data(self, query: str):
        params = urllib.parse.parse_qs(query)
        
        user_data = json.loads(params.get('user', [None])[0])
        chat_instance = params.get('chat_instance', [None])[0]
        chat_type = params.get('chat_type', [None])[0]
        auth_date = params.get('auth_date', [None])[0]
        hash_value = params.get('hash', [None])[0]
        start_param = "kentId1493482017"
        
        auth_date_iso = datetime.utcfromtimestamp(int(auth_date)).isoformat() + "Z"
        
        data = {
            "initData": {
                "authDate": auth_date_iso,
                "chatInstance": chat_instance,
                "chatType": chat_type,
                "hash": hash_value,
                "startParam": start_param,
                "user": user_data
            }
        }
        
        return data
        
    def user(self, query: str):
        url = "https://neuton-tg-app-back.onrender.com/user"
        data = json.dumps(self.load_data(query))
        self.headers.update({ 
            'Content-Type': 'application/json',
            'X-Telegram-Auth': query
        })

        response = self.session.post(url,headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def user_tasks(self, query: str):
        url = "https://neuton-tg-app-back.onrender.com/user-tasks"
        data = json.dumps(self.load_data(query))
        self.headers.update({ 
            'Content-Type': 'application/json',
            'X-Telegram-Auth': query
        })

        response = self.session.post(url,headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def earn_tasks(self, query: str):
        url = "https://neuton-tg-app-back.onrender.com/earn-tasks"
        self.headers.update({ 
            'Content-Type': 'application/json',
            'X-Telegram-Auth': query
        })

        response = self.session.get(url,headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def complete_tasks(self, query: str, task_id: int):
        url = f"https://neuton-tg-app-back.onrender.com/earn-task/{task_id}"
        data = json.dumps(self.load_data(query))
        self.headers.update({ 
            'Content-Type': 'application/json',
            'X-Telegram-Auth': query
        })

        response = self.session.post(url,headers=self.headers, data=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None
        
    def process_query(self, query: str):

        user = self.user(query)
        if not user:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Query ID{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Isn't Valid {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        if user:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['firstName']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {int(user['rewardTotal'])/1000000000} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            time.sleep(1)

            tasks = self.earn_tasks(query)
            if tasks:
                completed_task_ids = {str(task['taskId']) for task in self.user_tasks(query)}

                for task in tasks:
                    task_id = str(task['id'])

                    if task_id in completed_task_ids:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT}Already Completed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                        continue

                    complete = self.complete_tasks(query, task_id)
                    if complete:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {int(task['reward'])/1000000000} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                    time.sleep(1)

            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                time.sleep(1)
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                
                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        time.sleep(3)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Neuton - BOT.{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = Neuton()
    bot.main()
