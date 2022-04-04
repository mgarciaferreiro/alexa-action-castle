from game_classes import * 

def build_game():
    # Locations
    nowhere = Location("nowhere", "")

    cottage = Location("Cottage", "You are standing in a small cottage.")
    garden_path = Location("Garden Path", "You are standing on a lush garden path. There is a cottage here.")
    fishing_pond = Location("Fishing Pond", "You are at the edge of a small fishing pond.")
    winding_path = Location("Winding Path", "You are walking along a winding path. There is a tall tree here.")
    top_of_tree = Location("Top of the Tall Tree", "You are the top of the tall tree.")
    afterlife = Location("The Afterlife", "You are dead. GAME OVER.")
    afterlife.set_property('end_game', True)
    drawbridge = Location("Drawbridge", "You are standing on one side of a drawbridge leading to ACTION CASTLE.")
    courtyard = Location("Courtyard", "You are in the courtyard of ACTION CASTLE.")
    tower_stairs = Location("Tower Stairs", "You are climbing the stairs to the tower. There is a locked door here.")
    tower = Location("Tower", "You are inside a tower.")
    dungeon_stairs = Location("Dungeon Stairs", "You are climbing the stairs down to the dungeon.")
    dungeon = Location("Dungeon", "You are in the dungeon. There is a spooky ghost here")
    great_feasting_hall = Location("Great Feasting Hall", "You stand inside the Great Feasting Hall.")
    throne_room = Location("Throne Room", "This is the throne room of ACTION CASTLE.")

    # Connections
    cottage.add_connection("out", garden_path)
    garden_path.add_connection("south", fishing_pond)
    garden_path.add_connection("north", winding_path)
    winding_path.add_connection("up", top_of_tree)
    top_of_tree.add_connection("jump", afterlife)
    winding_path.add_connection("east", drawbridge)
    drawbridge.add_connection("east", courtyard)
    courtyard.add_connection("up", tower_stairs)
    tower_stairs.add_connection("up", tower)
    courtyard.add_connection("down", dungeon_stairs)
    dungeon_stairs.add_connection("down", dungeon)
    courtyard.add_connection("east", great_feasting_hall)
    great_feasting_hall.add_connection("east", throne_room)
    
    # Items that you can pick up
    lamp = Item("lamp", "a lamp", "A LAMP. ", start_at=None)
    fishing_pole = Item("pole", "a fishing pole", "A SIMPLE FISHING POLE.", start_at=cottage)
    rose = Item("rose", "a red rose", "IT SMELLS GOOD.",  start_at=None)
    fish = Item("fish", "a dead fish", "IT SMELLS TERRIBLE.", start_at=None)
    branch = Item("branch", "a stout, dead branch", "IT LOOKS LIKE IT WOULD MAKE A GOOD CLUB.", start_at=top_of_tree)
    key = Item("key", "a brass key", "THIS LOOKS USEFUL.", start_at=None)
    candle = Item("candle", "a strange candle", "THE CANDLE IS COVERED IN MYSTERIOUS RUNES.", start_at=great_feasting_hall)
    crown = Item("crown", "a crown", start_at=None)
    
    # Scenery (not things that you can pick up)
    pond = Item("pond", "a small fishing pond", "THERE ARE FISH IN THE POND.", start_at=fishing_pond)
    pond.set_property("gettable", False)
    rosebush = Item("rosebush", "a rosebush", "THE ROSEBUSH CONTAINS A SINGLE RED ROSE.  IT IS BEAUTIFUL.", start_at=garden_path)
    rosebush.set_property("gettable", False)
    troll = Item("troll", "a mean troll", "THE TROLL HAS A WARTY GREEN HIDE AND LOOKS HUNGRY.", start_at=drawbridge)
    troll.set_property("gettable", False)
    guard = Item("guard", "a guard carrying a sword and a key", start_at=courtyard)
    guard.set_property("gettable", False)
    door = Item("door", "a locked door", "THE DOOR IS LOCKED.", start_at=tower_stairs)
    door.set_property("gettable", False)
    princess = Item("princess", "A princess who is beautiful and lonely. She awaits her non-gender-stereotypical soulmate.", start_at=tower)
    princess.set_property("gettable", False)
    ghost = Item("ghost", "a ghost with bony, claw-like fingers and who is wearing a crown.", "LEGENDS SAY HE CAN ONLY BE DEFEATED WITH AN EXORCISM RITUAL.", start_at=dungeon)
    ghost.set_property("gettable", False)
    throne = Item("throne", "an ornate, golden throne", start_at=throne_room)
    throne.set_property("gettable", False)
    princess_heart = Item("princess' heart", "the princess' heart", start_at=None)
    princess_heart.set_property("gettable", False)
    
    # Blocks
    drawbridge.add_block("east", "The troll blocks your way", {"location_doesnt_have_item": troll})
    tower_stairs.add_block("up", "The door is locked", {"location_doesnt_have_item": door})
    dungeon_stairs.add_block("down", "It's too dark to see", {"inventory_contains": candle})
    courtyard.add_block("east", "The guard refuses to let you pass", {"location_doesnt_have_item": guard})

    # Add special functions to your items
    rosebush.add_action("pick rose",  add_item_to_inventory, (rose, "You pick the lone rose from the rosebush.", "You already picked the rose."))
    rose.add_action("smell rose",  describe_something, ("It smells sweet."))
    pond.add_action("catch fish",  describe_something, ("You reach into the pond and try to catch a fish with your hands, but they are too fast."))
    pond.add_action("catch fish with pole",  add_item_to_inventory, (fish, "You dip your hook into the pond and catch a fish.","You weren't able to catch another fish."), 
                  preconditions={"inventory_contains":fishing_pole})
    troll.add_action("hit troll with branch", end_game, ("The troll is much stronger than you and it tears you limb to limb. You have died. THE END."), 
                   preconditions={"inventory_contains":branch, "location_has_item": troll})
    troll.add_action("give fish to troll", destroy_item , (troll, "The troll runs off to eat the fish. You can now cross the bridge.", "You already tried that."), 
                   preconditions={"inventory_contains":fish, "location_has_item": troll})
    guard.add_action("hit guard with branch", hit_guard, (guard, key), 
                   preconditions={"inventory_contains": branch, "location_has_item": guard})
    door.add_action("unlock door", destroy_item, (door, "The door is unlocked.", "You already tried that"), 
                  preconditions={"inventory_contains": key})
    princess.add_action("talk to princess", describe_something, "The guards whisper that the ghost of the king haunts the dungeons as a restless spirit!")
    princess.add_action("give rose to princess", give_rose_to_princess, (princess, rose, princess_heart),
                      preconditions={"inventory_contains": rose})
    princess.add_action("kiss princess", describe_something, ("You and the princess share a beautiful, romantic kiss."),
                      preconditions={"inventory_contains": princess_heart})
    candle.add_action("light candle", add_item_to_inventory, (candle, "The candle is lit up.", "You already picked the candle."))
    candle.add_action("do exorcism", do_exorcism, (candle, ghost, crown),
                    preconditions={"location_has_item": ghost})
    candle.add_action("read runes", describe_something, ("The odd runes are part of an exorcism ritual used to dispel evil spirits."))
    throne.add_action("sit on throne", end_game , ("You are now the new ruler of Action Castle! THE END."))
    
    return Game(cottage)
            
            