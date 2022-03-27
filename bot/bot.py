import discord
import requests
import io


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)

        if message.content.startswith('```html'):
            # html_file = message.content

            # CURSED INCOMING. I want an HTML file to send to selenium, right? Why not create an io body?
            SCREENSHOT_NAME = ""
            
            with io.StringIO() as cursedFile:
                cursedFile.write(message.content)
                files = {'file' : cursedFile}
                # then post it
                r = requests.post(
                    'http://browser:3000', files=files)
                if r.content.decode() == "Screenshot requires POST to / with html content":
                    await message.reply('Failed on the request attempt. Contact bot developer')
                else:
                    SCREENSHOT_NAME = r.content.decode()
                
            if SCREENSHOT_NAME == "":
                await message.reply('Failed on getting screenshot name. Contact bot developer')
            else:
                r = requests.get(f"http://browser:3000/files/{SCREENSHOT_NAME}")
                with open(f"/tmp/{SCREENSHOT_NAME}","wb") as f:
                    f.write(r.content)
                    

                await message.reply(file=discord.File(f"/tmp/{SCREENSHOT_NAME}"))                    
                

                # print(r.headers)
                # print(r.status_code)
                # await message.reply()


            '''
            ```html
            <body>
                <div style="width: 500px;height: 500px; background-color: black;">
                    <h1>hello world</h1>
                </div>
                <img src="https://assets.bwbx.io/images/users/iqjWHBFdfxIU/i_.Hrdvci2bw/v1/1200x-1.jpg" alt="">    
            </body>
            ```
            '''

            # URL = 'https://www.yourlibrary.ca/account/index.cfm'

            # send file once I get it back

            # with open('my_image.png', 'rb') as f:
            #     picture = discord.File(f)
            #     await message.send(file=picture)


# intents = discord.Intents.default()
# intents.message_content = True

client = MyClient()

token = ""

# try:
#     with open("secret.key","wb") as s:
#         token = s.read()
#         print(token)
#         client.run(token)
# except:
#     print("Psst... put the discord token into the secret.key file")


with open("secret.key","rb") as s:
    token = s.read()
    print(token)
    client.run(token.decode())
