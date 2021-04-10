from helpers.experience_table import experience_table


def xp_to_level(self, experience):
    l = 0
    r = 99
    mid = None
    level = None

    if experience >= 13034431:
        level = 99
    else:
        # While the left is less than the right
        while l <= r:

            # The mid is halfway between the left and right
            mid = l + math.ceil((r - l) / 2);

            # Check if x is present at mid
            if experience_table[mid][1] <= experience < experience_table[mid + 1][1]:
                level = experience_table[mid][0]
                break
                # return level

            elif experience_table[mid + 1][1] == experience:
                level = experience_table[mid + 1][0]
                break

            # If x is greater, ignore left half
            elif experience_table[mid][1] < experience and experience_table[mid + 1][1] < experience:
                l = mid + 1

            # If x is smaller, ignore right half
            else:
                r = mid - 1

    # If we reach here, then the element was not present
    return level
