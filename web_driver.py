import chromedriver_binary
import time
from selenium import webdriver
from selenium.webdriver import common
import string

# Fill in credentials here.
server = 'tx3.' # Example url
username = 'User'
password = 'Passowrd'
home_url = 'https://' + server + 'travian.com/'




# Some options for the webdriver so it can operate in the background.
chrome_options = webdriver.ChromeOptions()
experimentalFlags = ['calculate-native-win-occlusion@2']
chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
chrome_options.add_experimental_option('localState',chromeLocalStatePrefs)

# Starting webdriver.
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.minimize_window




# Helper function - may need to use encode/decode and translation to
# remove unicode and punctuation. Not being used currently because the unicode
# on the site is inconsistent. May use an HTML parser in the future.
def remove_unicode(s):
    """
    Removes unicode characters and punctuation from string and converts to an
    int that is then returned.
    """
    # Uses encode/decode to remove unicode. Then, translate function to remove
    # punctuation. Works oddly in some instances.
    # s.strip().encode('ascii', 'ignore').decode().translate(str.maketrans('', '', string.punctuation))
    s.strip().encode('ascii', 'ignore').decode()




# Execution functions: Use these to navigate through the UI.
def start():
    """
    Navigates to login page url.
    """
    driver.get(home_url)

def login():
    """
    Uses username and password to log in on the login page. If cookies appear,
    rejects them.
    """
    # Reject cookies.
    try:
        driver.find_element_by_class_name('cmpboxbtnno').click() # Cookie element may change in future.
    except:
        pass
    
    # Use credential to log into account.
    finally:
        driver.find_element_by_name('name').send_keys(username)
        driver.find_element_by_name('password').send_keys(password)
        driver.find_element_by_name('s1').click() # Clicks submit button.

# May have to change these commands for multiple villages, but navigating via dorf
# works fine with only 1 village.
def switch_to_fields(): # TODO switch by clicking icon rather than url.
    """
    Switches to field view using dorf url.
    """
    driver.get(home_url + 'dorf1.php')

def switch_to_buildings(): # TODO switch by clicking icon rather than url.
    """
    Switches to building view using dorf url.
    """
    driver.get(home_url + 'dorf2.php')

def click_resource_slot(slot_number):
    """
    Clicks a resource field on resource view. Slots are numbered 1-18 and have
    different resource types depending on village type and gid value. Will use
    resource scanner to get building slot and then this function to click into
    specified field.
    """
    driver.find_element_by_class_name('buildingSlot' + str(slot_number)).click()

def click_building_slot(slot_number): # TODO: new construction on random slot.
    """
    Clicks a building slot on the buildings view. Slots are numbered 19-40 and
    have different building types depending on what you build in each. Should
    use click_building_id in most instances, but this will be useful when
    selecting a slot to place a new building.
    
    Main building = 26
    Rally point = 39
    Wall = 40
    """
    driver.find_element_by_class_name('a' + str(slot_number)).click()
    
def click_building_id(id_num):
    """
    Uses the building ID found from scan_buildings to click into a building
    slot.

    Parameters
    ----------
    id_num : STRING ('g#')
    """
    driver.find_element_by_class_name(id_num).click()

def click_build():
    """
    On the build screen, clicks the build button.
    """
    # TODO: Click the ad for faster building.
    # Finish checkbox and warning message handling.
    # Add handling in case buttons are gold instead of green.
    
    # POSSIBLE FUTURE IMPLEMENTATION
    # try:
    #     driver.find_element_by_class_name('videoFeatureButton').click()
    #     try:
    #         driver.find_element_by_class_name('checkbox').click()
    #         driver.find_element_by_id('videoFeature').find_element_by_class_name('buttonFramed').click()
    #     except:
    #         pass
    # except:
        # driver.find_element_by_class_name('section1').find_element_by_class_name('green').click()
    
    # For now, just click the normal build button if it is green.
    driver.find_element_by_class_name('section1').find_element_by_class_name('green').click()

def click_adventures():
    """
    Clicks hero adventure icon.
    """
    driver.find_element_by_class_name('content').click()

def start_adventure():
    """
    Starts the adventure when on the adventure screen. Always selects top adventure.
    """
    driver.find_element_by_class_name('gotoAdventure').click()

def click_hero_portrait():
    """
    Clicks the hero image button.
    """
    driver.find_element_by_id('heroImageButton').click()

def click_send_troops():
    """
    Clicks the send troops tab from the rally point.
    """
    driver.find_element_by_class_name('favorKey2').click()
    
def click_overview():
    """
    Clicks overview tab from the rallypoint.
    """
    driver.find_element_by_class_name('normal').click()

def send_attack(unit, quantity, x, y, atk_type): #TODO add checking for max quantity units.
    """
    takes unit type, qunatity, x and y coordinates, and attack type, then
    sends an attack.

    Parameters
    ----------
    unit : STR
        leg, EI, ram, sen, pra, EI, cat, set, imp, EC
    quantity : INT
    x : INT
    y : INT
    atk_type : STR
        raid, normal, or rein

    Returns
    -------
    None.

    """
    unit_codes = {'leg': ('0', 't1'),
                  'el': ('0', 't4'),
                  'ram': ('0', 't7'),
                  'sen': ('0', 't9'),
                  'pra': ('0', 't2'),
                  'ei': ('0', 't5'),
                  'cat': ('0', 't8'),
                  'set': ('0', 't10'),
                  'imp': ('0', 't3'),
                  'ec': ('0', 't6'),}
    
    # Enter troop quantity. Lowers passed unit string before searching dict.
    driver.find_element_by_name('troops[' + unit_codes[unit.lower()][0] + '][' + unit_codes[unit.lower()][1] + ']').send_keys(quantity)
    
    # Enter attack type
    if atk_type == 'rein':
        driver.find_element_by_xpath("//div[@class='option']/label[1]").click()
    if atk_type == 'normal':
        driver.find_element_by_xpath("//div[@class='option']/label[2]").click()
    if atk_type == 'raid':
        driver.find_element_by_xpath("//div[@class='option']/label[3]").click()
    
    # Input x and y values
    driver.find_element_by_name('x').send_keys(x)
    driver.find_element_by_name('y').send_keys(y)
    
    # Submit
    driver.find_element_by_name('s1').click()
    
    # Confirm
    driver.find_element_by_id('btn_ok').click()
    
def build_troops(qty):
    # TODO Generalize this function so it is passed troop type. Only builds legionnaires so far.
    """
    Builds troops.
    
    qty: INT
    
    Returns
    -------
    None.

    """
    switch_to_buildings()
    time.sleep(1)
    click_building_slot(23)
    time.sleep(1)
    
    # Right now this function only builds legionnaires.
    possible_troops = driver.find_element_by_xpath("//div[@class='innerTroopWrapper troop1 ']/div[@class='details']/div[@class='cta']/a").get_attribute('innerHTML')
    print(possible_troops)
    inp = driver.find_element_by_xpath("//div[@class='action troop troop1 ']/div[@class='innerTroopWrapper troop1 ']/div[@class='details']/div[@class='cta']/input[@class='text']")
    if int(possible_troops) >= 0:
        inp.send_keys(qty)
    else:
        return
    time.sleep(1)
    driver.find_element_by_xpath("//div[@class='contentContainer']/div[@id='content']/div[@id='build']/form/button[@id='s1']").click()
    time.sleep(1)

# This is the end of the execution functions.








# Data collection functions.
def check_page(): # TODO: currently an unused function.
    """
    Checks what the current page is and returns string of page type. This is
    currently unused by the rest of the program but may come in handy when
    handling of multiple villages is implemented.
    
    RETURNS
    -------
    string:
        login
    """
    # Checks if on login page.
    if (driver.current_url == home_url + 'login.php' or
        driver.current_url == home_url + 'logout.php'):
        return 'login'
    else:
        return 'unkown'

def check_adventures():
    """
    Checks if there is an adventure and returns True if there is one. Looks at
    the adventure icon to see if it is a number.
    """
    el = int(driver.find_element_by_class_name('content').get_attribute('innerHTML')) > 0
    return el

def read_resources():
    # The resource storage data is currently unused by program, but may be used
    # later if more complex planning is implemented. Free crop is currently used.
    """
    Reads and returns a list of the current stored resource in the village as
    well as storage capacities and free crop. Returns list of ints.
    
    RETURNS
    -------
    list[wood, clay, iron, crop, warehouse, granary, free crop]
    """
    # ALTERNATIVE IMPLEMENTATION for if I ever figure out remove unicode.
    # result = [int(remove_unicode(driver.find_element_by_id('l1').get_attribute('innerHTML'))),
    #         int(remove_unicode(driver.find_element_by_id('l2').get_attribute('innerHTML'))),
    #         int(remove_unicode(driver.find_element_by_id('l3').get_attribute('innerHTML'))),
    #         int(remove_unicode(driver.find_element_by_id('l4').get_attribute('innerHTML'))),
    #         int(remove_unicode(driver.find_element_by_xpath("//div[@class='warehouse']/div[@class='capacity']/div[@class='value']").get_attribute('innerHTML'))),
    #         int(remove_unicode(driver.find_element_by_xpath("//div[@class='granary']/div[@class='capacity']/div[@class='value']").get_attribute('innerHTML'))),
    #         int(remove_unicode(driver.find_element_by_id("stockBarFreeCrop").get_attribute('innerHTML')))]
    
    # Webdriver and HTML are funky so this is the only way I found I could reliably get values.
    return [int(driver.find_element_by_id('l1').get_attribute('innerHTML').translate(str.maketrans('', '', string.punctuation))),
            int(driver.find_element_by_id('l2').get_attribute('innerHTML').translate(str.maketrans('', '', string.punctuation))),
            int(driver.find_element_by_id('l3').get_attribute('innerHTML').translate(str.maketrans('', '', string.punctuation))),
            int(driver.find_element_by_id('l4').get_attribute('innerHTML').translate(str.maketrans('', '', string.punctuation))),
            int(driver.find_element_by_xpath("//div[@class='warehouse']/div[@class='capacity']/div[@class='value']").get_attribute('innerHTML').translate(str.maketrans('', '', string.punctuation)).encode('ascii', 'ignore').decode()),
            int(driver.find_element_by_xpath("//div[@class='granary']/div[@class='capacity']/div[@class='value']").get_attribute('innerHTML').translate(str.maketrans('', '', string.punctuation)).encode('ascii', 'ignore').decode()),
            int(driver.find_element_by_id("stockBarFreeCrop").get_attribute('innerHTML').translate(str.maketrans('', '', string.punctuation)).encode('ascii', 'ignore').decode())]

def read_production():
    """
    Reads and returns a list of current resource production rates of village.
    Must be on resource view of village. Returns list of ints. Essentially
    reads the side table.

    Returns
    -------
    list[wood, clay, iron, crop]
    """
    # Locates numbers in production table and puts them in a list.
    L = driver.find_element_by_id('production').find_elements_by_class_name('num')
    result = []
    
    # Iterates through table numbers and formats them into ints. Returns list of
    # production numbers.
    for element in L:
        result.append(element.get_attribute('innerHTML').strip())
        # result.append(int(element.get_attribute('innerHTML').strip().encode('ascii', 'ignore').decode()))
    for i in range(len(result)):
        result[i] = int(result[i].encode('ascii', 'ignore').decode())
    return result

def read_army():
    """
    Gets army in current village from overview tab of rally point.

    Returns
    -------
    list:
        list containing INTs for each unit type.

    """
    result = []
    unit_cells = driver.find_element_by_xpath("//table[@class='troop_details']/tbody[@class='units last']").find_elements_by_tag_name('td')
    for cell in unit_cells:
        result.append(int(cell.get_attribute('innerHTML')))
    return result

def scan_resource_fields():
    """
    Creates list of lists of resource fields and returns it. Each element in
    tile list is string. Must be on field view of village.

    Returns
    -------
    [[status, level, colorLayer, gid#, buildingSlot#, '', and level#]]
    
    """
    result = []
    
    # Iterates through tile numbers and grabs tile info. Appends tiles to result.
    for i in range(1, 19):
        title = driver.find_element_by_class_name('buildingSlot' + str(i)).get_attribute('class')
        L = title.split(' ')
        result.append(L)
    return result

def scan_buildings():
    """
    Creates a list of lists of buildings in current village and returns it. Each
    tile element is a string. Must be on building view.

    Returns
    -------
    [[buildingSlot, a#, g#, aid#, roman, buildingLVL]]
      All strings in list. g# is building ID.

    """
    result = []
    
    # Iterates through building tile numbers, grabbing tile information and
    # appending tile to list to return.
    for i in range(19, 41):
        tile = driver.find_element_by_class_name('a' + str(i)).get_attribute('class')
        L = tile.split(' ')
        L += [driver.find_element_by_class_name('a' + str(i)).find_element_by_xpath("//div[@class='labelLayer']").get_attribute('innerHTML').strip()]
        result.append(L)
    return result

def building_current_level(slot_num): # TODO This function may or may not be redundant.
    pass

def current_construction():
    """
    Creates a list of tuples specifying what is currently being constructed in village.

    Returns
    -------
    [(Name of construction, level#, seconds remaining), ...]

    """
    result = []
    
    # See if something is even being built.
    try:
        building_list = driver.find_element_by_class_name('buildingList').find_elements_by_tag_name('li')
        for building in building_list:
            result.append(building.find_element_by_class_name('name').get_attribute('innerHTML').strip())
        return result
    except:
        return result
    
    # Find building elements and build them into a list.
    currently_building = building_list.find_elements_by_tag_name('li')
    
    # Iterate through list, appending each building tuple to result before returning.
    for e in currently_building:
        name = e.find_element_by_class_name('name').get_attribute('innerHTML')
        level = e.find_element_by_class_name('lvl').get_attribute('innerHTML')
        duration = e.find_element_by_class_name('timer').get_attribute('value')
        result.append((name, level, duration))
    return result

def current_hero_HP():
    """
    When on hero page, finds current HP and returns value.

    Returns
    -------
    INT
        Hero HP
    """
    # Locates element using xpath.
    health = driver.find_element_by_xpath("//tr[@class='attribute health tooltip']/td[@class='element current powervalue']/span[@class='value']").get_attribute('innerHTML')
    
    # Removes unicode, converts to int, and returns.
    return int(health.encode('ascii', 'ignore').decode()[:-1])

def incoming_attack():
    """
    Detects if there is an incoming attack and returns the time to it landing. Returns 0 if no attack.
    """
    try:
        driver.find_element_by_xpath("//table[@id='movements']/tbody/tr[2]/td[2]/div[@class='mov']/span[@class='a1']")
        time_left = driver.find_element_by_xpath("//table[@id='movements']/tbody/tr[2]/td[2]/div[@class='dur_r']/span[@class='timer']").get_attribute('innerHTML')
        t = time_left.split(':')
        seconds = int(t[0])*60*60 + int(t[1])*60 + int(t[2])
        return seconds
    except:
        return 0


