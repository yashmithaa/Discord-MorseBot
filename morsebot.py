import config
import hikari
import lightbulb
import random


bot = lightbulb.BotApp(
    token=config.TOKEN,
    prefix = 'dino ',
    intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT, 
    default_enabled_guilds=(GuildId)
)

@bot.listen(hikari.StartedEvent)
async def onstart(event):
    
    print("Bot is now online")

morse_code ={'A':'.-', 'B':'-...', 'C': '-.-.', 'D': '-..',
                'E' : '.', 'F':'..-.', 'G':'--.','H':'....','I':'..',
                'J':'.---','K':"-.-", 'L':".-..", 'M':'--', "N":'-.',
                'O' : '---','P': '.--.', 'Q':'--.-','R':'.-.','S':'...',
                'T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
                '1': '.----', '2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...',
                '8':'---..','9':'----.','0':'-----',' ':'/'}


@bot.command
@lightbulb.command('hello','Dino wants to say hello')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx):    
    await ctx.respond("Hello I'm Dino. Nice to meet you!")

@bot.command
@lightbulb.command('cute','Dino blushes')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx):    
    await ctx.respond("Hehe so are you ;)")

@bot.command
@lightbulb.option('letter','Enter a letter')
@lightbulb.command('teach','To find the code of a particular letter/number')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    choice = ctx.options.letter.upper()
    await ctx.respond(morse_code[choice])

@bot.command
@lightbulb.command('revise','Makes you revise morse-code from A-Z')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx):
    for letter in morse_code:
        this = letter + ' : '+ morse_code[letter]
        await ctx.respond(this)

@bot.command
@lightbulb.option('text','Enter the text you wanna translate',modifier=lightbulb.OptionModifier.GREEDY)
@lightbulb.command('morse','Translates text to morse code')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx):
    translated=''
    
    listToStr = ' '.join([str(elem) for elem in ctx.options.text])
    sentence = listToStr.upper()
    sample = sentence
    if sample.replace(' ','').isalpha()==True:
        for letter in sentence:
            
            if letter==' ':
                translated = translated + ' / '
            else:
                translated = translated + ' ' + morse_code[letter] + ' '
        await ctx.respond("`"+translated+"`")
    else:
        await ctx.respond("Invalid. Use alphabet and numbers ;)")
    
def get_key(val):
    for key, value in morse_code.items():
        if val == value:
            return key

@bot.command
@lightbulb.option('morse','Enter the code you wanna translate',modifier=lightbulb.OptionModifier.GREEDY)
@lightbulb.command('text','Translates morse code to text')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx):
    translated=''
    
    code = ctx.options.morse
    
    for i in code:
        if i=='/':
            translated = translated + ' '
        if i in morse_code.values():
            key = get_key(i)
            translated = translated  + key 
        '''else:
            translated = translated + ' error '''
    await ctx.respond(translated.lower())

@bot.command
@lightbulb.command('avatar','shows off your cool avatar')
@lightbulb.implements(lightbulb.PrefixCommand)
async def message(ctx):
    user = ctx.author

    embed = hikari.Embed(description='Here you go!')
    embed.set_image(user.avatar_url)
    embed.set_author(name = str(user),icon=str(user.avatar_url))
    await ctx.respond(embed)
    
    

@bot.listen(hikari.GuildMessageCreateEvent)
async def print_msg(event):
    return event.content
        
        
    

@bot.command
@lightbulb.command('quiz','letter,word or sentence quiz')
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def quiz(ctx):
    embed = hikari.Embed(title='Yay It\'s Quiz time',description='This is dino. Let\'s test your morse code knowledge\n\n`dino quiz letter` : for a quiz in letters\n\n`dino quiz word` : for a quiz in words',
    colour='E8E8E8')
    await ctx.respond(embed)

@quiz.child
@lightbulb.command('letter', 'letter quiz')
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def letterquiz(ctx:lightbulb.Context):
    score = 0
    for i in range(5):
        answer, question = random.choice(list(morse_code.items()))

        embed = hikari.Embed(title='Letter quiz', description="You have 8s to answer\n" + question)
        await ctx.respond(embed)

        def predicate(event: hikari.GuildMessageCreateEvent)->bool:
            message = event.message
            assert message.content is not None
            return (message.author == ctx.author) and (message.content.lower() == answer.lower())

        try:
            message = await bot.wait_for(
                hikari.GuildMessageCreateEvent, 
                timeout=8, 
                predicate=predicate
            )
            assert message.content is not None
            if message.content.lower() == answer.lower():
                score+=10
                await ctx.respond("GG correct")
            else:
                pass
        except TimeoutError:
            await ctx.respond("Time's up!\nCorrect answer was `" + answer + "`")
    
    embed = hikari.Embed(title='Results!!', description="Your score is "+str(score)+"/50",colour='E8E8E8')
    await ctx.respond(embed)
    
morse_code_words = {
    "hello": ".... . .-.. .-.. ---",
    "meow": "-- . . --- .--",
    "cat": "-.-. .- -",
    "dog": "-.. --- --.",
    "bark": "-... .- .-. -.-",
    "liquid": ".-.. ..- --.- .. - .. -..",
    "parking": ".--. .- .-. -.- .. -. --.",
    "lid": ".-.. .. -..",
    "pretty": ".--. .-. . - - -.--",
    "melon": "-- . .-.. --- -.",
    "lemon": ".-.. . -- --- -.",
    "cute": "-.-. ..- - .",
    "dino": "-.. .. -. ---",
    "meme": "-- . -- .",
    "world": ".-- --- .-. .-.. -..",
    "happy": ".... .- .--. .--. -.--",
    "annoy": ".- -. -. --- -.--",
    "sad": "... .- -..",
    "tap": "- .- .--.",
    
}
   
@quiz.child
@lightbulb.command('word','word quiz')
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def wordquiz(ctx:lightbulb.Context):
    score = 0
    for i in range(5):
        answer, question = random.choice(list(morse_code_words.items()))

        embed = hikari.Embed(title='Word quiz', description="You have 15s to answer\n `" + question+"`")
        await ctx.respond(embed)

        def predicate(event: hikari.GuildMessageCreateEvent)->bool:
            message = event.message
            assert message.content is not None
            return (message.author == ctx.author) and (message.content.lower() == answer.lower())

        try:
            message = await bot.wait_for(
                hikari.GuildMessageCreateEvent, 
                timeout=8, 
                predicate=predicate
            )
            assert message.content is not None
            if message.content.lower() == answer.lower():
                score+=10
                await ctx.respond("GG correct")
            else:
                pass
        except TimeoutError:
            await ctx.respond("Time's up!\nCorrect answer was `" + answer + "`")
    
    embed = hikari.Embed(title='Results!!', description="Your score is "+str(score)+"/50",colour='E8E8E8')
    await ctx.respond(embed)



bot.run(status=hikari.Status.IDLE,activity=hikari.Activity(
        name=" dino help ",
        type=hikari.ActivityType.LISTENING,
    ))