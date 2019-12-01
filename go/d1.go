package main

import (
	"bufio"
	"io"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
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
	fuelNeeded := 0

	file, err := os.Open(fn)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	line := ""
	mass := 0
	for {
		line, err = reader.ReadString('\n')
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		mass, err = strconv.Atoi(strings.TrimSpace(line))
		fuelNeeded += fuelFromMass(int(mass))
	}
	log.Printf("[1] fuel needed: %d\n", fuelNeeded)
	return fuelNeeded
}

func part2(fn string) int {
	fuelNeeded := 0

	file, err := os.Open(fn)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	line := ""
	mass := 0
	fuel := 0
	for {
		line, err = reader.ReadString('\n')
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		mass, err = strconv.Atoi(strings.TrimSpace(line))
		if err != nil {
			log.Fatal(err)
		}
		fuel = fuelFromMass(mass)
		fuelNeeded += fuel + fuelFromFuel(fuel)
	}
	log.Printf("[2] fuel needed: %d\n", fuelNeeded)
	return fuelNeeded
}

func main() {
	fn := "../res/d1.txt"
	part1(fn)
	part2(fn)
}
