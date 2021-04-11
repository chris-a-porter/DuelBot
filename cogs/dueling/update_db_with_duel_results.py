import psycopg2

# Update the winne and loser's kill/death in the database


async def update_db_with_duel_results(self, winner, loser):
    # 1st command for the winner
    # 2nd command for the loser
    # gp included in case user has never had row created for them
    commands = (
        f"""
    INSERT INTO duel_users (user_id, nick, wins, losses, gp)
    VALUES
    ({winner.id}, '{str(loser.id)}', 1, 0, 0)
    ON CONFLICT (user_id) DO UPDATE
    SET wins = duel_users.wins + 1, nick = '{str(winner.id)}'
    """,

        f"""
    INSERT INTO duel_users (user_id, nick, wins, losses, gp)
    VALUES
    ({loser.id}, '{str(loser.id)}', 0, 1, 0)
    ON CONFLICT (user_id) DO UPDATE
    SET losses = duel_users.losses + 1 , nick = '{str(loser.id)}'
    """
    )

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        for command in commands:
            cur.execute(command) # Do the SQL shit

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("SOME ERROR 1", error)
    finally:
        if conn is not None:
            conn.close()