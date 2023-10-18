import datetime
import requests
import telebot
import time
import json
import csv

class WebScraper:
    
    def __init__(self):
        # EDIT!
        self.game = "AVIÃOZINHO->"
        self.token = '******'
        self.chat_id = '******'
        self.url_API = '********'
        self.gales = 1
        self.link = '[Clique aqui!](https://estrelabet.com/en/games/detail/casino/normal/7787)'
        
        
       # MAYBE EDIT!
        self.win_results = 0
        self.loss_results = 0
        self.max_hate = 0
        self.win_hate = 0


        # NO EDIT!
        self.count = 0
        self.analisar = True
        self.alvo = 0
        self.message_delete = False
        self.bot = telebot.TeleBot(token=self.token, parse_mode='MARKDOWN')
        self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.check_date = self.date_now

    def restart(self):
        if self.date_now != self.check_date:           
            print('Reiniciando o robô!')
            self.check_date = self.date_now
            
            self.bot.send_sticker(
                self.chat_id, sticker='CAACAgEAAxkBAAEBbJJjXNcB92-_4vp2v0B3Plp9FONrDwACvgEAAsFWwUVjxQN4wmmSBCoE')
            self.results()

            #ZERA OS RESULTADOS
            self.win_results = 0
            self.loss_results = 0
            self.max_hate = 0
            self.win_hate = 0
            self.bot.send_message(chat_id=self.chat_id, text=('🚧 Atualizando os algoritmos! 🚧'))
            time.sleep(3540)

            self.bot.send_sticker(
                self.chat_id, sticker='CAACAgEAAxkBAAEBPQZi-ziImRgbjqbDkPduogMKzv0zFgACbAQAAl4ByUUIjW-sdJsr6CkE')
            self.results()
            return True
        else:
            return False

    def results(self):

        if self.win_results + self.loss_results != 0:
            a = 100 / (self.win_results + self.loss_results) * self.win_results 
        else:
            a = 0
        self.win_hate = (f'{a:,.2f}%')


        self.bot.send_message(chat_id=self.chat_id, text=(f'''

► PLACAR GERAL = ✅{self.win_results}  |  🚫{self.loss_results} 
► Consecutivas = {self.max_hate}
► Assertividade = {self.win_hate}
    
    '''))
        return
       
    def alert_sinal(self):
        message_id = self.bot.send_message(
            self.chat_id, text='''
⚠️ ANALISANDO, FIQUE ATENTO!!!
''').message_id
        self.message_ids = message_id
        self.message_delete = True
        return
    
    def alert_gale(self):
        self.message_ids = self.bot.send_message(self.chat_id, text=f'''⚠️ Vamos para o {self.count}ª GALE''').message_id
        self.message_delete = True
        return

    def delete(self):
        if self.message_delete == True:
            self.bot.delete_message(chat_id=self.chat_id,
                                    message_id=self.message_ids)
            self.message_delete = False
      
    def send_sinal(self, finalnum):
        self.analisar = False
        self.bot.send_message(chat_id=self.chat_id, text=(f'''

🚀 *ENTRADA CONFIRMADA!* 🚀

🎰 Apostar após o {finalnum}x
🎯 Sair em {self.alvo}x 
🔁 Fazer até {self.gales} gales

📱 *{self.game}* '''f'{self.link}''''

    '''))
        return

    def martingale(self, result):

        if result == "WIN":
            print(f"WIN")
            self.win_results += 1
            self.max_hate += 1
            # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuhtkFBbPbho5iUL3Cw0Zs2WBNdupaAACQgQAAnQVwEe3Q77HvZ8W3y8E')
            self.bot.send_message(chat_id=self.chat_id, text=(f'''✅✅✅ WIN ✅✅✅'''))
        
        elif result == "LOSS":
            self.count += 1
            
            if self.count > self.gales:
                print(f"LOSS")
                self.loss_results += 1
                self.max_hate = 0
                #self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuh9kFBbVKxciIe1RKvDQBeDu8WfhFAACXwIAAq-xwEfpc4OHHyAliS8E')
                self.bot.send_message(chat_id=self.chat_id, text=(f'''🚫🚫🚫 LOSS 🚫🚫🚫'''))
                time.sleep(1)
                self.bot.send_message(chat_id=self.chat_id, text=(f'🚧 Analisando os Algoritmos! 🚧'))
                time.sleep(600)

            else:
                print(f"Vamos para o {self.count}ª gale!")
                self.alert_gale()
                return
            
            

        self.count = 0
        self.analisar = True
        self.results()
        self.restart()
        return

    def check_results(self, results):

        if results >= self.alvo:
            self.martingale('WIN')
            return
        
        elif results < self.alvo:
            self.martingale('LOSS')
            return

    def start(self):
        check = []
        while True:
            try:
                self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))

                results = []
                time.sleep(1)

                response = requests.get(self.url_API)
                json_data = json.loads(response.text)
                for i in json_data['results']:
                    results.append(float(i))

                if check != results:
                    check = results
                    self.delete()
                    self.estrategy(results)
                
            except:
                print("ERROR - 404!")
                continue

    def estrategy(self, results):
        print(results[0:59])

        if self.analisar == False:
            self.check_results(results[0])
            return

        # EDITAR ESTRATÉGIAS
        elif self.analisar == True:  

            


            #ESTRATÉGIAS COM MANUAIS
            if results[0] >= 5 and results[1] >= 5 and results[2] >= 5:
                print("SINAL ENCONTRADO!")
                self.alvo = 1.5
                self.send_sinal(results[0])
                return
            
            #ALERTA DAS MANUAIS
            if results[0] >= 5 and results[1] >= 5:
                self.alert_sinal()
                return
            

scraper = WebScraper()
scraper.start()