def check_over_50_over_under(lines):
    if len(lines) > 7 and float(lines[7]) > 50:
        # If number is over 100, add a decimal point after the second character, if  not add it after the first character
        if float(lines[7]) > 100:
            lines[7] = lines[7][:2] + '.' + lines[7][2:]
        else:
            lines[7] = lines[7][:1] + '.' + lines[7][1:]


def check_over_40_points(lines):
    if len(lines) > 2 and float(lines[2]) > 40:
        # Add a decimal point after the first character
        lines[2] = lines[2][:1] + '.' + lines[2][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 2 and len(lines[2]) > 1 and lines[2][0] == '0' and lines[2][1] != '.':
        lines[2] = lines[2][:1] + '.' + lines[2][1:]


def check_over_5_PF(lines):
    if len(lines) > 6 and float(lines[6]) > 5:
        # Add a decimal point after the first character
        lines[6] = lines[6][:1] + '.' + lines[6][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 6 and len(lines[6]) > 1 and lines[6][0] == '0' and lines[6][1] != '.':
        lines[6] = lines[6][:1] + '.' + lines[6][1:]


def check_over_20_3P(lines):
    if len(lines) > 5 and float(lines[5]) > 20:
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]
    elif len(lines) > 5 and float(lines[5]) * 3 > float(lines[2]):
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]
    elif len(lines) > 5 and float(lines[5]) * 3 == float(lines[2]) and (float(lines[4]) != 0 or float(lines[3]) != 0):
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[5]) > 1 and lines[5][0] == '0' and lines[5][1] != '.':
        lines[5] = lines[5][:1] + '.' + lines[5][1:]


def check_over_20_2FG(lines):
    if len(lines) > 4 and float(lines[4]) > 20:
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]
    elif len(lines) > 4 and float(lines[4]) * 2 > float(lines[2]):
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]
    elif len(lines) > 4 and float(lines[4]) * 2 == float(lines[2]) and (float(lines[3]) != 0 or float(lines[5]) != 0):
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[4]) > 1 and lines[4][0] == '0' and lines[4][1] != '.':
        lines[4] = lines[4][:1] + '.' + lines[4][1:]


def check_over_30_FT(lines):
    if len(lines) > 3 and float(lines[3]) > 30:
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
    elif len(lines) > 3 and float(lines[3]) > float(lines[2]):
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
        print("Free throws are over the total points")
    elif len(lines) > 3 and float(lines[3]) == float(lines[2]) and (float(lines[4]) != 0 or float(lines[5]) != 0):
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
        print("Free throws are equal to the total points")

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[3]) > 1 and lines[3][0] == '0' and lines[3][1] != '.':
        lines[3] = lines[3][:1] + '.' + lines[3][1:]


def check_minutes(lines):
    if len(lines) > 1 and ':' not in lines[1]:
        # After the first two chars, add the colon
        lines[1] = lines[1][:2] + ':' + lines[1][2:]
        # After the fifth char, add the following numbers to the next line
        lines.insert(2, lines[1][5:])
        # Remove the numbers from the first line
        lines[1] = lines[1][:5]

    print("Lines after minutes check: ", lines)


def double_check_points(lines):
    if len(lines) > 5:
        free_throws_pts = float(lines[3]) * 1
        two_points_pts = float(lines[4]) * 2
        three_points_pts = float(lines[5]) * 3
        total_points = float(lines[2])
        # I want to check if the points match but give a certain amount of possible error, up to 1 point
        if abs(free_throws_pts + two_points_pts + three_points_pts - total_points) > 1:
            print("Points don't match")
            print(f"Free throws: {free_throws_pts}, 2 points: {two_points_pts}, 3 points: {three_points_pts}, total: {total_points}")
            # Add a decimal point after the first character
            lines[2] = lines[2][:1] + '.' + lines[2][1:]


def check_data(lines):
    check_minutes(lines)
    check_over_40_points(lines)
    check_over_30_FT(lines)
    check_over_20_2FG(lines)
    check_over_20_3P(lines)
    check_over_5_PF(lines)
    check_over_50_over_under(lines)
    double_check_points(lines)
