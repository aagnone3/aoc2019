package main

import (
	"log"
	"math"
	"strconv"
)

func fuelFromMass(mass int) int {
	return int(math.Floor(float64(mass)/3.0) - 2)
}

func fuelFromFuel(fuelMass int) int {
	fuelNeeded := 0
	done := false
	for done == false {
		fuelMass = fuelFromMass(fuelMass)
		if fuelMass > 0 {
			fuelNeeded += fuelMass
		} else {
			done = true
		}
	}
	return fuelNeeded
}

func part1(fn string) int {
	numLines := countNumLines(fn)
	out := make([]int, numLines)

	process := func(i int, line string) {
		mass, err := strconv.Atoi(line)
		if err != nil {
			log.Fatal(err)
		}
		out[i] = fuelFromMass(int(mass))
	}
	readFileLines(fn, numLines, process)

	fuelNeeded := 0
	for _, num := range out {
		fuelNeeded += num
	}
	log.Printf("[1] fuel needed: %d\n", fuelNeeded)
	return fuelNeeded
}

func part2(fn string) int {
	numLines := countNumLines(fn)
	out := make([]int, numLines)

	process := func(i int, line string) {
		mass, err := strconv.Atoi(line)
		if err != nil {
			log.Fatal(err)
		}
		fuel := fuelFromMass(int(mass))
		out[i] = fuel + fuelFromFuel(fuel)
	}
	readFileLines(fn, numLines, process)

	fuelNeeded := 0
	for _, num := range out {
		fuelNeeded += num
	}
	log.Printf("[2] fuel needed: %d\n", fuelNeeded)
	return fuelNeeded
}

func main() {
	fn := "../res/d1.txt"
	part1(fn)
	part2(fn)
}
