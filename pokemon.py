import sys
#known bugs to resolve in future iterations--

#known improvements and features to implement--
#each time pokemon wins a fight, give them experience
#each time pokemon reaches certain experience, they can evolve
#create inheritence classes with more pokemon from the Pokemon class


#Create Pokemon class with methods:
# 1. attack - type advantages included
# 2. lose_health 
# 3. regain_health
# 4. knock out a pokemon, when pokemons health would reach 0
# 5. revive knocked out pokemon - probably dont use yet
class Pokemon:
    def __init__(self, name, level, type, knocked_out=False):
        self.name = name #we can remove this when we complete the first iteration. this will be an inherited class at one point
        self.type = type #we can remove this when we complete the first iteratio
        self.level = level 
        self.max_health = 900+level*100 #this will be determined by the pokemons level
        self.current_health = self.max_health
        self.knocked_out = knocked_out

    def attack(self, pokemon):
        self.damage = 500 +  self.level*200
        for type in type_relations[self.type]:
            if type == pokemon.type:
                self.damage *= 2
                break
        print("\n{name} deals {damage} damage".format(name=self.name, damage=self.damage))
        return self.damage

    def regain_health(self, hp_boost):
        # health_before = self.current_health
        self.current_health += hp_boost
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        return self.current_health

    def lose_health(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0
        print("\n{} lost {} hp. Current hp: {}".format(self.name, damage, self.current_health))
        return self.current_health

    def knockout(self): #maybe always call this out whenever a pokemon attacks
        if self.current_health <= 0:
            print("\n{name} has reached 0 hp and has been knocked out!".format(name=self.name))
            self.knocked_out = True
            return self.knocked_out
        return self.knocked_out

    def revive(self):
        self.knocked_out = False
        self.current_health = self.max_health*0.5
        return "\n{name} has has been revived to {hp} hp".format(name=self.name, hp=self.current_health)

#Create Trainer class with methods:
# 1. attack other trainer's pokemon
# 2. use a potion - need to add logic so trainer cant use more than the potions in inventory
# 3. choose pokemon- this will set the active pokemon

class Trainer:
    def __init__(self, name, pokemons, potions=1):
        self.name = name
        self.potions = potions
        self.current_pokemon = None
        if len(pokemons) > 6:
            self.pokemons = 0
            print("\nTotal amount of pokemon chosen must not exceed 6, please try again")
        else:
            self.pokemons = pokemons  #this will be a list of all pokemon you choose

    def choose_pokemon(self, pokemon): 
        if pokemon.knocked_out == True:
            print("\n{} has been knocked and cannot be chosen, please choose another pokemon".format(pokemon.name))
            return None
        elif pokemon not in self.pokemons:
            print("\n{} is not available, please choose another pokemon".format(pokemon.name))
            return None           
        else:
            self.current_pokemon = pokemon
            print("\n{} has chosen {}".format(self.name, self.current_pokemon.name))
            return self.current_pokemon

    def use_potion(self): 
        if self.current_pokemon.knocked_out == True:
            print("\n{} has been knocked and cannot regain health!".format(self.current_pokemon.name))
            return None
        else:
            self.current_pokemon.regain_health(500)
            print("\n{} used a potion on {} and now has {} hp!".format(self.name, self.current_pokemon.name, self.current_pokemon.current_health))
        
    def attack_other_trainer(self, other_trainer):
        if self.current_pokemon.knocked_out == True:
            print("\n{} is knocked out and cannot attack, please select another pokemon".format(self.current_pokemon.name))
            return None
        their_pokemon=other_trainer.current_pokemon
        print("\n{} attacks {} with {}".format(self.name, their_pokemon.name, self.current_pokemon.name))
        their_pokemon.lose_health(self.current_pokemon.attack(their_pokemon))
        their_pokemon.knockout()

    def all_pokemon_KO(self):
        for pokemon in self.pokemons:
            if pokemon.knocked_out == False:
                return False
        return True

#create pokemon relationships
type_relations = {
    "Fire" : ["Grass", "Steel", "Ice"], 
    "Water" : ["Fire", "Rock", "Ice"], 
    "Grass" : ["Water", "Rock"], 
    "Electric" : ["Water", "Flying", "Normal"], 
    "Rock" : ["Electric", "Flying"], 
    "Flying" : ["Grass", "Fighting"], 
    "Fighting" : ["Rock", "Normal"], 
    "Steel" : ["Rock", "Ice"], 
    "Ice" : ["Grass", "Flying"], 
    "Normal":["Normal"]
    }
#create pokemons - we can create inherited classes after initial implementation
charmander = Pokemon("Charmander", 1, "Fire")
squirtle = Pokemon("Squirtle", 1, "Water")
bulbasaur = Pokemon("Bulbasaur", 1, "Grass")
eevee = Pokemon("Eevee", 1, "Normal")
arcanine = Pokemon("Arcanine", 3, "Fire")
pikachu = Pokemon("Pikachu", 2, "Electric")
onix = Pokemon("Onix", 2, "Rock")
steelix = Pokemon("Steelix", 2, "Rock")
salamence = Pokemon("Salamence", 4, "Flying")
machamp = Pokemon("Machamp", 3, "Fighting")
snorlax = Pokemon("Snorlax", 3, "Normal")
magnemite = Pokemon("Magnemite", 2, "Steel")
lapras = Pokemon("Lapras", 2, "Ice")

########################################################################################################### PLAY GAME ##################################################################################################################

available_pokemon = [charmander, squirtle, bulbasaur, eevee, arcanine, pikachu, onix, steelix, salamence, snorlax, magnemite]
player1_pokemon = []
player2_pokemon = []

def str_to_class(str): #method to change string to class object
    return getattr(sys.modules[__name__], str)

#allow players to choose up to number_of_pokemon
number_of_pokemon = 2 #can be 6 but we'll start with letting them choose 3 pokemon
count = 0
while count < number_of_pokemon*2:
    if count%2==0:
        player_string = "Player 1" 
        player = player1_pokemon
    else:
        player_string = "Player 2" 
        player = player2_pokemon     

    try:
        print("----------------------------------")   
        chosen_pokemon = input("\n{}: choose from the following pokemon and enter the name:\n\n {}\n\n".format(player_string, [pokemon.name for pokemon in available_pokemon]))
        class_chosen_pokemon = str_to_class(chosen_pokemon.lower())
        player.append(class_chosen_pokemon)
        available_pokemon.remove(class_chosen_pokemon)
        count += 1
    except AttributeError:
        print("----------------------------------")
        print("\nInvalid pokemon choice, please try again\n")


player1 = Trainer("Player 1", player1_pokemon)
player2 = Trainer("Player 2", player2_pokemon)


#let each player select their starting pokemon - need to fix case where opposing player chooses the same players pokemon
invalid_choice = True
count = 0
while count < 2:
    if count%2==0:
        player_string = "Player 1" 
        player = player1
        player_pokemon = player1_pokemon
    else:
        player_string = "Player 2" 
        player = player2
        player_pokemon = player2_pokemon 
    print("----------------------------------")
    try:
        chosen_pokemon = input("\n{}, Choose your pokemon by entering their name:\n\n {}\n\n".format(player_string, [pokemon.name for pokemon in player_pokemon]))
        class_chosen_pokemon = str_to_class(chosen_pokemon.lower())
        # player.choose_pokemon(class_chosen_pokemon)
        # count += 1
        if player.choose_pokemon(class_chosen_pokemon) != None:
            count += 1
    except AttributeError:
        print("----------------------------------")
        print("\nInvalid pokemon choice, please try again\n")       


#player1 and player2 will alternate in turns until one player has all their pokemon knocked out, starting with player1
count = 0
while player1.all_pokemon_KO() == False and player2.all_pokemon_KO() == False:
    if count%2==0:
        current_player = player1
        opposing_player = player2
        current_player_string = "Player1"
    else:
        current_player = player2
        opposing_player = player1
        current_player_string = "Player2"

    print("----------------------------------")           
    print("\n{}'s turn\n".format(current_player_string))
    invalid_choice = True
    while invalid_choice == True:
        if current_player.current_pokemon.knocked_out == True:
            print("----------------------------------")
            print("\n{} is knocked out\n".format(current_player.current_pokemon.name))
            print("----------------------------------")
            try:
                switch_pokemon = input("\nWhich Pokemon would you like to switch in (enter name)? :\n\n {}\n\n".format([pokemon.name for pokemon in current_player.pokemons]))
                switch_pokemon = str_to_class(switch_pokemon.lower())
                if current_player.choose_pokemon(switch_pokemon) == None:
                    invalid_choice = True
                else:
                    invalid_choice = False
            except AttributeError:
                print("----------------------------------")
                print("\nInvalid pokemon choice, please try again\n")
                invalid_choice = True                
        else:
            print("----------------------------------")
            choice = input("\nWhat would you like to do? Input number for choice:\n[1] Attack opposing pokemon\n[2] Use potion on current pokemon\n[3] Switch Pokemon\n\n")
            if choice == "1":
                current_player.attack_other_trainer(opposing_player)
                invalid_choice = False
            elif choice == "2": 
                if current_player.potions == 0:
                    print("----------------------------------")
                    print("No more potions remaining, please select another choice")
                    invalid_choice = True
                else:
                    current_player.use_potion()
                    invalid_choice = False
            elif choice == "3":
                print("----------------------------------")
                try:
                    switch_pokemon = input("\nWhich Pokemon would you like to switch in (enter name)? :\n\n {}\n\n".format([pokemon.name for pokemon in current_player.pokemons]))
                    switch_pokemon = str_to_class(switch_pokemon.lower())
                    if current_player.choose_pokemon(switch_pokemon) == None:
                        invalid_choice = True
                    else:
                        invalid_choice = False
                except AttributeError:
                    print("----------------------------------")
                    print("\nInvalid pokemon choice, please try again\n")
                    invalid_choice = True                                    
            else:
                print("----------------------------------")
                print("\nInvalid choice, please select again")
    count += 1

if player1.all_pokemon_KO() == True:
    print("----------------------------------")
    print("\nPlayer 1 is the victor!")
else:
    print("----------------------------------")
    print("\nPlayer 2 is the victor!")


########################################################################################################### END GAME ##################################################################################################################



