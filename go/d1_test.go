package main

import "testing"

func TestFuelFromMass(t *testing.T) {
	nums := map[int]int{
		12:     2,
		14:     2,
		1969:   654,
		100756: 33583,
	}
	for mass, expected := range nums {
		computed := fuelFromMass(mass)
		if computed != expected {
			t.Errorf("Expected %d , got %d\n", expected, computed)
		}
	}

}

func TestFuelFromFuel(t *testing.T) {
	nums := map[int]int{
		100756: 50346,
	}
	for fuel, expected := range nums {
		computed := fuelFromFuel(fuel)
		if computed != expected {
			t.Errorf("Expected %d , got %d\n", expected, computed)
		}
	}

}

func TestPart1(t *testing.T) {
	exp := 3361299
	got := part1("../res/d1.txt")
	if exp != got {
		t.Errorf("Expected %d, got %d", exp, got)
	}
}

func TestPart2(t *testing.T) {
	exp := 5039071
	got := part2("../res/d1.txt")
	if exp != got {
		t.Errorf("Expected %d, got %d", exp, got)
	}
}
