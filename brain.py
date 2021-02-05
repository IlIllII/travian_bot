import web_driver as WD
import random
import time
import timer
import string


# TODO might implement farmlist operation later on.
# farm_list = [('Leg', 2, 41, -15, 'raid')]


# Here are the building codes I have discovered. You can find more by inspecting the HTML
# of the webpage. Use these to make your build queue.
"""
building ids:
    g0  = empty slot
    g10 = warehouse
    g11 = granary
    g13 = smithy
    g15 = main building
    g16 = rally point
    g17 = marketplace
    g18 = embassy
    g19 = barracks
    g20 = stable
    g22 = academy
    g23 = cranny
    g25 = residence
    g31 = wall
"""

# This is so they can't tell its a bot playing ;)
def sleep(a, b):
    time.sleep(random.randint(a, b))


# TODO Might implement more advanced logic later.
# class ResourceTile():
#     def __init__(self):
#         self.lvl = lvl
#         self.resource = resource
#         self.tile = tile


def can_build_field():
    """
    Checks to see if a field is currently being constructed. If so, returns
    False. If not, returns True.
    """
    # Creates resouce labels to search with.
    resource_labels = ('Clay P',
                       'Woodcu',
                       'Iron M',
                       'Cropla')
    
    # Uses web_driver to get a list of what is currently being constructed.
    current_construction = WD.current_construction()
    
    # Does some operations to determine if a field is being constructed and
    # returns if able to build.
    if len(current_construction) == 0:
        return True
    for t in current_construction: # Checks to see if its a resource field being built.
        for r in resource_labels:
            if t[0] == r:
                return False
    return True

def can_build_building():
    """
    Checks to see if a building is currently being constructed. If so, returns
    False. If not, returns True.
    """
    # Creates resouce labels to search with.
    resource_labels = ('Clay P',
                       'Woodcu',
                       'Iron M',
                       'Cropla')
    
    # Uses web_driver to get a list of what is currently being constructed
    current_construction = WD.current_construction()
    
    # Does some operations to determine if a building is being constructed and
    # returns if able to build.
    if len(current_construction) == 0:
        return True
    if len(current_construction) == 2:
        return False
    for t in current_construction:
        for r in resource_labels:
            if t[0] == r:
                return True
    return False

def format_fields():
    """
    Uses webdriver to collect field information, formats it, and creates a model
    in the form of a sorted list of lists.

    Returns
    -------
    [[clay fields], [wood fields], [iron fields], [crop fields]]
    
    resource tiles = [[status, level, colorLayer, gid#, buildingSlot#, '', and level#], ...]

    """
    # Initializes lists to fill in with resource tiles.
    clay = []
    wood = []
    iron = []
    crop = []
    
    # Webdriver gets resource tiles.
    resource_tiles = WD.scan_resource_fields().copy()
    
    # Iterates through tiles, converting level and buildingSlot str to int and sorting into
    # new lists based on resource type as denoted by 'gid#'.
    for tile in resource_tiles:
        tile[-1] = int(tile[-1][5:])
        tile[4] = int(tile[4][12:])
        # Append the tile to list based on resource type
        if tile[3] == 'gid1':
            wood.append(tile)
        elif tile[3] == 'gid2':
            clay.append(tile)
        elif tile[3] == 'gid3':
            iron.append(tile)
        else:
            crop.append(tile)
    
    # Sorts each resource list based on tile levels.
    clay.sort(key=lambda x: x[-1])
    wood.sort(key=lambda x: x[-1])
    iron.sort(key=lambda x: x[-1])
    crop.sort(key=lambda x: x[-1])
    
    # Recombines resource tiles into sorted list and returns it.
    # Organizing the data makes it handy for deciding what to build next.
    fields = [clay, wood, iron, crop]
    return fields

def field_planner():
    # TODO adapt for capital building with res lvls above 10.
    """
    Takes formatted fields and selects which field to build. Includes logic that
    selects the lowest level resource tile depending on max res lvl 10 and
    crop production/free crop.

    Returns
    -------
    INT
        returns the building slot number of the resource tile to build.

    """
    production = WD.read_production()
    resources = format_fields()
    free_crop = WD.read_resources()[6]
    
    # Used to maintain 10/12/8/6 production ratios.
    crop_is_sufficient = production[1]/2 < production[3]
    
    # Are there any fields to upgrade?
    all_fields_max = True
    for resource in resources:
        for tile in resource:
            if tile[6] != 10:
                all_fields_max = False
    
    # Are all fields but croplands maxed? This is so we know
    # when to push crop fields above the production ratio.
    non_crop_max = True
    for resource in resources[:3]:
        for tile in resource:
            if tile[6] != 10:
                non_crop_max = False
    
    # Return for when we don't want to upgrade anything.
    if all_fields_max:
        return None
    
    # Conditions for upgrading crop fields before other resources.
    if non_crop_max or crop_is_sufficient == False or free_crop < 10:
        for tile in resources[3]:
            if tile[0] == 'good':
                return tile[4]
    
    # Otherwise we upgrade resource fields according to what we can afford
    # starting with clay, then wood, then iron. Because of the costs of upgrading
    # each field type, we will naturally approach the ideal production ratio by
    # following this algorithm.
    for resource in resources[:3]:
        for tile in resource:
            if tile[0] == 'good':
                return tile[4]

def upgrade_resource_field():
    """
    Switches to fields, scans fields, decides what to upgrade, then executes
    upgrade.

    Returns
    -------
    None.

    """
    WD.switch_to_fields()
    tile_number = field_planner()
    if tile_number != None:
        WD.click_resource_slot(tile_number)
        WD.click_build()

def building_planner(): # TODO we will implement this later perhaps
    """
    Decides what to build when on buildings view of village.

    Returns
    -------
    None.

    """
    
    slots = WD.scan_buildings()
    for slot in slots:
        pass

def read_build_queue():
    """
    This is to get the build queue from the text file. Returns a list of buildings
    with their desired levels.
    """
    build_queue = []
    queue = open('build_queue.txt')
    for line in queue:
        L = line.split(',')
        t = L[0], L[1]
        build_queue.append(t)
    queue.close()
    return build_queue
    
def execute_build_queue(build_queue):
    """
    Pass this function read_build_queue().
    
    Tile data = [[buildingSlot, a#, g#, aid#, roman, buildingLVL]]
    
    Executes the build queue straight through until it cannot afford
    one of the buildings.

    Parameters
    ----------
    build_queue : List of buildings and desired levels

    Returns
    -------
    None.

    """
    
    WD.switch_to_buildings()
    sleep(1,2)
    buildings = WD.scan_buildings()
    building_exists = False
    building_maxed = False
    for ID, LVL in build_queue:
        for building in buildings:
            if building[2] == ID:
                building_exists = True
                if int(building[5]) < int(LVL):
                    # building_slot = int(building[1][1:])
                    # WD.click_building_slot(building_slot)
                    WD.click_building_id(ID)
                    sleep(1, 3)
                    WD.click_build()
                else:
                    building_maxed = True
    if building_exists and building_maxed and len(build_queue) > 1:
        execute_build_queue(build_queue[1:])
    elif building_exists == False and len(build_queue) > 1:
        execute_build_queue(build_queue[1:])

def upgrade_building(building_id, final_level): # TODO Fix this, execute build queue is better.
    """
    builds 

    Parameters
    ----------
    building_id : TYPE
        DESCRIPTION.
    final_level : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    WD.switch_to_buildings()
    buildings_list = WD.scan_buildings()
    building_exists = False
    already_maxed = False
    if can_build_building() == True:
        for building in buildings_list:
            if building[2] == building_id:
                building_exists = True
                if int(building[5]) < final_level:
                    building_slot = int(building[1][1:])
                    WD.click_building_slot(building_slot)
                    sleep(1, 3)
                    WD.click_build()
                else:
                    already_maxed = True
    if building_exists == False:
        # build new building in a random slot
        pass

def get_army_dict():
    """
    Reads army from rally point overview and returns a dict with troop numbers

    Returns
    -------
    d : dict

    """
    # Navigates to rally point troop overview
    WD.switch_to_buildings()
    sleep(1, 2)
    WD.click_building_slot(39)
    sleep(1, 2)
    WD.click_overview()
    army = WD.read_army()
    
    # Gets information from table of troops in village.
    d = {'Leg': army[0],
         'Pra': army[1],
         'Imp': army[2],
         'EL': army[3],
         'EI': army[4],
         'EC': army[5],
         'Ram': army[6],
         'Cat': army[7],
         'Sen': army[8],
         'Set': army[9],
         'Hero': army[10]}
    return d

def send_raids(farm_list): # TODO this function is unused currently. Instead, use the cycler function.
    """
    uses farmlist to send raids. Collects army information. If there is enough
    army for the raid list, sends out raids.

    Parameters
    ----------
    farm_list : TYPE
        DESCRIPTION.
    army_dict : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    flag = True
    troops_req = {}
    WD.switch_to_buildings()
    WD.click_building_slot(39)
    WD.click_overview()
    army_dict = get_army_dict()
    for raid in farm_list:
        if raid[0] not in troops_req:
            troops_req[raid[0]] = 0
        troops_req[raid[0]] += raid[1]
    for key in troops_req:
        if army_dict[key] < troops_req[key]:
            flag = False
    if flag == True:
        for raid in farm_list:
            WD.switch_to_buildings()
            sleep(1, 3)
            WD.click_building_slot(39)
            sleep(1, 3)
            WD.click_send_troops()
            sleep(1, 5)
            WD.send_attack(raid[0], raid[1], raid[2], raid[3], raid[4])
            sleep(1,3)

def read_cycle(cycler_doc):
    """
    Reads the cycler.txt file to get the current farm list.
    """
    cycle = []
    cycle_doc = open(cycler_doc)
    for line in cycle_doc:
        f = line.strip('\n').split(',')
        f[1], f[2], f[3] = int(f[1]), int(f[2]), int(f[3])
        cycle.append(f)
    cycle_doc.close()
    return cycle

def write_cycle(cycle, cycler_doc): # rewrite cycle
    """
    Rotates the farm list by one and rewrites to the cycle file.
    """
    f = open(cycler_doc, 'w')
    for i in range(len(cycle)):
        if i != len(cycle)-1:
            f.write(cycle[i][0] + ',' + str(cycle[i][1]) + ',' + str(cycle[i][2]) + ',' + str(cycle[i][3]) + ',' + cycle[i][4])
            f.write('\n')
        else:
            f.write(cycle[i][0] + ',' + str(cycle[i][1]) + ',' + str(cycle[i][2]) + ',' + str(cycle[i][3]) + ',' + cycle[i][4])
    f.close()

def cycle_raids(cycler_doc):
    """
    This sends raids found in the cycler file farm list. Goes raid by raid until there
    are not enough troops in the village. This is more efficient than sending a farm list
    with gold club, but is really only feasible with a small army because it is time intensive
    manually sending tons of raids.
    """
    troops_left = True
    while troops_left == True:
        cycle = read_cycle(cycler_doc)
        troops = get_army_dict()
        print(troops[cycle[0][0]] >= cycle[0][1])
        if troops[cycle[0][0]] >= cycle[0][1]:
            WD.click_send_troops()
            sleep(1,3)
            WD.send_attack(cycle[0][0], cycle[0][1], cycle[0][2], cycle[0][3], cycle[0][4])
            print('Troops sent')
        else:
            print('not enough troops')
            print(troops)
            troops_left = False
            break
        cycle = cycle[1:] + [cycle[0]]
        write_cycle(cycle, cycler_doc)
        sleep(1,3)

def hero_adventure():
    """
    Sends hero on adventure if it exists.
    """
    adventure_exists = WD.check_adventures()
    print(adventure_exists)
    if adventure_exists:
        army = get_army_dict()
        if army['Hero'] == 1:
            WD.click_hero_portrait()
            sleep(1,3)
            HP = WD.current_hero_HP()
            if HP > 30:
                WD.click_adventures()
                sleep(1,3)
                WD.start_adventure()
                sleep(1,3)
                print('Adventure sent.')
    
                

# These functions constitute the main program and implement all the previous functions and
# webdriver functions. They all try to execute their contents so the program doesn't crash if you
# click something or something unexpected happens like an update.
def run():
    """
    Navigates to the login page and logs in.
    """
    WD.start()
    sleep(1,2)
    WD.login()
    sleep(3,5)
    
def hero():
    """
    Sends hero adventure.
    """
    try:
        hero_adventure()
        print('Adventure processed')
    except:
        print('Adventure error')
    sleep(1,5)

def fields():
    """
    Upgrades fields.
    """
    try:
        upgrade_resource_field()
        print('Fields processed')
    except:
        print('Fields error')
    sleep(1,5)

def buildings():
    """
    Executes build queue.
    """
    try:
        execute_build_queue(read_build_queue())
        print('Buildings processed')
    except:
        print('Buildings error')
    sleep(1, 5)

def train():
    """
    Trains troops. Input desired qty here.
    """
    try:
        WD.build_troops(1)
        print('Training processed')
    except:
        print('Training error')
    sleep(1,5)

def cycler():
    """
    Sends raids by going through leg, imp, and EI cycler text files.
    """
    try:
        cycle_raids('leg_cycler.txt')
        print('Leg cycler processed')
    except:
        print('Leg cycler error')
    sleep(1,5)
    
    try:
        cycle_raids('imp_cycler.txt')
        print('Imp cycler processed')
    except:
        print('Imp cycler error')
    sleep(1,5)
    
    try:
        cycle_raids('EI_cycler.txt')
        print('EI cycler processed')
    except:
        print('EI cycler error')
    sleep(1,5)

# Here is the main program to run. Change the opts list if you
# want the script to execute only certain tasks. Also, adjust the
# sleep schedule and timing at the bottom however you like. If the
# program runs 24/7 you will get banned. With these settings I have
# not been banned.
def program():
    iterations = 1
    while True:
        # Shuffle task order
        # opts = [hero, cycler, fields, buildings, train]
        opts = [hero, cycler, fields, buildings]
        random.shuffle(opts) # To be less predictable for the MH.
        
        print('Iteration ' + str(iterations))
        
        # Execute tasks
        run()
        for i in range(len(opts)):
            opts[i]()
        
        # Sleep
        sleep(1,5)
        WD.driver.get('https://www.google.com/')
        
        hour = time.localtime().tm_hour
        print('Current hour: ' + str(hour))
        print('Hour greater than 6 but less than 24: ' + str(6 < hour < 24))
        if 5 < hour < 24:
            duration = random.randint(15*60, 30*60)
        else:
            duration = random.randint(70*60, 100*60)
        
        # Dodge incoming attacks. Automatically adjusts sleep time depending on
        # when an attack will land. Right now only sends raids to dodge, will need to
        # update code to handle other troop types besides raiders.
        atk = WD.incoming_attack()
        if atk > 0:
            if atk > duration:
                pass
            elif atk < 300:
                duration = 5
            elif atk > 300 and atk < duration:
                duration = atk - 120
        print('Sleeping for ' + str(duration) + ' seconds...')
        print(time.localtime())
        iterations += 1
        time.sleep(duration)

