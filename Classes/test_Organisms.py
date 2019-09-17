import pytest
from Organisms import *


def test_init():
    organism_obj = Organism()
    fish_obj = Fish()
    bird_obj = Bird()
    mammal_obj = Mammal()

    assert type(organism_obj) is Organism
    assert type(fish_obj) is Fish
    assert type(bird_obj) is Bird
    assert type(mammal_obj) is Mammal

    assert organism_obj.age == 0

    mutations_init = {'first': True, 'second': False}

    mutated_org = Organism(mutations_init)
    assert mutated_org.mutations == mutations_init

    with pytest.raises(TypeError):
        assert Organism({'first': False, 'second': 2019})


def test_breed():
    org_male = Organism({'first': True, 'second': False, 'third': False})
    org_male.is_male = True
    org_female = Organism({'first': True, 'second': False})
    org_female.is_male = False

    org_child = org_female + org_male

    assert type(org_child) is Organism
    assert org_child.mutations == {'first': True, 'second': False}

    org_male.mother = org_female
    org_female.mother = org_female
    assert not (org_female + org_male).is_alive


def test_eat():
    old_fish = Fish()
    old_fish.age = 3
    young_fish = Fish()
    bird = Bird()

    assert old_fish.is_alive and young_fish.is_alive and bird.is_alive
    # can't eat itself. Expect False
    assert not (old_fish - old_fish)
    # bird can't swim. Expect False
    assert not (young_fish - bird)
    # youngling try to eat elder. Expect False
    assert not (old_fish - young_fish)
    # successful eating
    assert (young_fish - old_fish)
    # fish can't fly. Expect False
    assert not (bird - old_fish)
    # dead can't eat. Expect False
    assert not (old_fish - young_fish)
    # but necrophagy is possible.
    assert (young_fish - old_fish)
