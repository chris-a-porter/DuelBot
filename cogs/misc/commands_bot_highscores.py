import discord
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def hs(self, ctx, *args):
    # Send a placehlder message
    placeholderEmbed = discord.Embed(title="DuelBot highscores", description="Checking the highscores...",
                                     color=discord.Color.gold())
    msg = await ctx.send(embed=placeholderEmbed)

    statList = ['attack', 'strength', 'defence', 'ranged', 'magic', 'hitpoints', 'herblore', 'prayer', 'slayer']
    iconDict = {'attack': 'https://oldschool.runescape.wiki/images/f/fe/Attack_icon.png?b4bce',
                'strength': 'https://oldschool.runescape.wiki/images/1/1b/Strength_icon.png?e6e0c',
                'defence': 'https://oldschool.runescape.wiki/images/b/b7/Defence_icon.png?ca0cd',
                'ranged': 'https://oldschool.runescape.wiki/images/1/19/Ranged_icon.png?01b0e',
                'magic': 'https://oldschool.runescape.wiki/images/5/5c/Magic_icon.png?334cf',
                'hitpoints': 'https://oldschool.runescape.wiki/images/9/96/Hitpoints_icon.png?a4819',
                'herblore': 'https://oldschool.runescape.wiki/images/0/03/Herblore_icon.png?ffa9e',
                'prayer': 'https://oldschool.runescape.wiki/images/f/f2/Prayer_icon.png?ca0dc',
                'slayer': 'https://oldschool.runescape.wiki/images/2/28/Slayer_icon.png?cd34f'}

    # Retrieve the total level highscores
    async def getTotalLevelHighscores():
        sql = f"""
           SELECT US.user_id, US.attack_xp, US.strength_xp, US.defence_xp, US.ranged_xp, US.magic_xp, US.hitpoints_xp, US.prayer_xp, US.herblore_xp, US.slayer_xp, DU.id
           FROM (user_skills US
           LEFT JOIN duel_users DU ON US.user_id = DU.user_id)
           """

        conn = None
        leaderboard = []

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)

            rows = cur.fetchall()

            for row in rows:
                leaderboard.append(row)

            return leaderboard

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 4", error)
            return leaderboard
        finally:
            if conn is not None:
                conn.close()
            return leaderboard

    async def getLevelHighscores(stat):
        sql = f"""
           SELECT US.user_id, US.{stat}_xp, DU.id
           FROM (user_skills US
           LEFT JOIN duel_users DU ON US.user_id = DU.user_id)
           """

        conn = None
        leaderboard = []

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(sql)

            rows = cur.fetchall()

            for row in rows:
                leaderboard.append(row)

            return leaderboard

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("SOME ERROR 4", error)
            return leaderboard
        finally:
            if conn is not None:
                conn.close()
            return leaderboard

    # The default highscores
    if len(args) == 0 or (len(args) == 1 and args[0].lower() == 'total'):

        totalLevelHighscores = await getTotalLevelHighscores()

        highscoresMessage = ""

        topPlayerCount = 0

        topScorers = []

        for person in totalLevelHighscores:

            print(person)

            # Row contains user id, attack, strength, defence, ranged, magic, hitpoints, prayer, herblore, slayer, nick in that order
            totalLevel = 0

            for n in range(1, 10):
                totalLevel = totalLevel + Skilling(self.bot).xpToLevel(person[n])

                print(person[0], totalLevel, n)

            topScorers.append([person[10], totalLevel])

        def returnTotal(elem):
            return elem[1]

        print(topScorers)
        topScorers.sort(key=returnTotal, reverse=True)
        print("SORTED:", topScorers)
        print(len(topScorers))

        for n in range(0, 10):
            if n < len(topScorers):
                highscoresMessage = highscoresMessage + f"{n + 1} - **{topScorers[n][0]}:** {topScorers[n][1]}\n"

        embed = discord.Embed(title="Overall Highscores", description=highscoresMessage, color=discord.Color.gold())
        embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/b/bd/Stats_icon.png?1b467')

        await msg.edit(embed=embed)
        return

    if args[0].lower() == 'wins' or args[0].lower() == 'kd':
        async def getWinsHighscores(ctx):
            sql = f"""
               SELECT nick, wins, losses
               FROM duel_users
               ORDER BY wins DESC
               """

            conn = None
            leaderboard = []

            try:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute(sql)

                rows = cur.fetchall()

                counter = 0
                for row in rows:
                    leaderboard.append(row)
                    counter += 1
                    if counter == 10:
                        return leaderboard

                cur.close()
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("SOME ERROR 4", error)
                return leaderboard
            finally:
                if conn is not None:
                    conn.close()
                return leaderboard

        # For when we have different high scores
        # if args == None:
        frontPage = await getWinsHighscores(ctx)

        description = ""

        if len(frontPage) == 0:
            errorEmbed = discord.Embed(title="Wins Highscores", description="Something went wrong.",
                                       color=discord.Color.dark_red())
            await msg.edit(embed=errorEmbed)

        for n in range(0, len(frontPage)):
            description += f"{n + 1} - **{frontPage[n][0]}**: {frontPage[n][1]} wins | {frontPage[n][2]} losses | {round((frontPage[n][1] / frontPage[n][2]), 2)} KDA \n"

        frontPageEmbed = discord.Embed(title="Wins Highscores", description=description, color=discord.Color.gold())
        await msg.edit(embed=frontPageEmbed)

    elif args[0].lower() in statList:
        levelHighscores = await getLevelHighscores(args[0].lower())

        highscoresMessage = ""

        topPlayerCount = 0

        topScorers = []

        for person in levelHighscores:
            # Row contains user id, stat, nick in that order
            level = Skilling(self.bot).xpToLevel(person[1])

            topScorers.append([person[2], level])

        def returnTotal(elem):
            return elem[1]

        topScorers.sort(key=returnTotal, reverse=True)

        for n in range(0, 10):
            if n < len(topScorers):
                highscoresMessage = highscoresMessage + f"{n + 1} - **{topScorers[n][0]}:** {topScorers[n][1]}\n"

        embed = discord.Embed(title=f"{args[0].lower().capitalize()} Highscores", description=highscoresMessage,
                              color=discord.Color.gold())
        embed.set_thumbnail(url=iconDict[args[0].lower()])

        await msg.edit(embed=embed)
        return

    elif args[0].lower() == 'gp':
        async def getGPHighscores(ctx):
            sql = f"""
               SELECT nick, gp
               FROM duel_users
               ORDER BY gp DESC
               """

            conn = None
            leaderboard = []

            try:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                cur.execute(sql)

                rows = cur.fetchall()

                counter = 0
                for row in rows:
                    leaderboard.append(row)
                    counter += 1
                    if counter == 10:
                        return leaderboard

                cur.close()
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("SOME ERROR 4", error)
                return leaderboard
            finally:
                if conn is not None:
                    conn.close()
                return leaderboard

        frontPage = await getGPHighscores(ctx)

        description = ""

        if len(frontPage) == 0:
            errorEmbed = discord.Embed(title="DuelBot Highscores", description="Something went wrong.",
                                       color=discord.Color.dark_red())
            await msg.edit(embed=errorEmbed)

        for n in range(0, 10):
            commaMoney = "{:,d}".format(int(frontPage[n][1]))
            description += f"{n + 1} - **{frontPage[n][0]}**: {commaMoney} GP\n"

        frontPageEmbed = discord.Embed(title="GP highscores", description=description, color=discord.Color.gold())
        await msg.edit(embed=frontPageEmbed)


    else:
        embed = discord.Embed(title="DuelBot highscores",
                              description="Could not find those hiscores. To view a specific hiscore, use =hs [type]",
                              color=discord.Color.gold())
        embed.set_thumbnail(url='https://oldschool.runescape.wiki/images/8/8c/HiScores_icon.png?99743')
        embed.add_field(name='Options',
                        value='**Attack\nStrength\nDefence\nRanged\nMagic\nHitpoints\nPrayer\nHerblore\nSlayer\nTotal\nGP\nWins**')

        await msg.edit(embed=embed)
        return
