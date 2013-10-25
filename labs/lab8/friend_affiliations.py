from mrjob.job import MRJob

class MRFriendAffiliations(MRJob):

    def mapper(self, _, line):
        # Tokenize line.
        tokens = line.split(',')
        tokens = [t.strip() for t in tokens]
        
        # First token is the person's name.
        # Second token is their favorite team.
        # Remaining tokens are their friends' names.
        name, team, friends = (tokens[0], tokens[1], tokens[2:])

        # Emit (key, value) pairs with friends names as the keys and 
        # (this_name, this_team) as the value (same value for all).
        for friend in friends:
            yield friend, (name, team)

        # Special case: emit a similar (key, value) pair for this person.
        yield name, (name, team)

    def reducer(self, name, friends):
        # Count the number of Red Sox and Cardinals fans who are friends
        # with this person.
        team = None
        red_sox_count = 0
        cardinals_count = 0
        for friend in friends:
            # Keep an eye out of the special case where the friends name 
            # and this persons name are the same -- that tells us which 
            # team this person cheers for.
            if friend[0] == name:
                this_team = friend[1]
            else:
                if friend[1] == "Red Sox":
                    red_sox_count += 1
                elif friend[1] == "Cardinals":
                    cardinals_count += 1
                else:
                    print "ERROR: Unknown team \"{0}\"".format(friend[1])

        # Yield results.
        yield name, (this_team, red_sox_count, cardinals_count)

if __name__ == '__main__':
    MRFriendAffiliations.run()

