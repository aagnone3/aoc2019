package main

import (
	"bufio"
	"context"
	"io"
	"log"
	"os"
	"runtime"
	"strings"

	"golang.org/x/sync/semaphore"
)

func countNumLines(fn string) int {
	file, err := os.Open(fn)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	numLines := 0
	reader := bufio.NewReader(file)
	for {
		_, err = reader.ReadString('\n')
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		numLines++
	}
	return numLines
}

func readFileLines(fn string, numLines int, process func(int, string)) {
	ctx := context.TODO()

	var (
		maxWorkers = runtime.GOMAXPROCS(0)
		sem        = semaphore.NewWeighted(int64(maxWorkers))
	)

	file, err := os.Open(fn)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	// process the lines of the file, using at most `maxWorkers` goroutines
	for i := 0; i < numLines; i++ {
		// acquire a semaphore lock before performing any work
		if err := sem.Acquire(ctx, 1); err != nil {
			log.Printf("Failed to acquire semaphore: %v\n", err)
			break
		}

		line, err := reader.ReadString('\n')
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		go func(i int) {
			defer sem.Release(1)
			process(i, strings.TrimSpace(line))
		}(i)
	}

	// Acquire all of the semaphore tokens, in order to ensure all goroutines
	// have finished.
	if err := sem.Acquire(ctx, int64(maxWorkers)); err != nil {
		log.Printf("Failed to acquire semaphor in final collect: %v\n", err)
	}
}
