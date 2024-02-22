package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"sync"
	"time"
)

func fetchData(urls []string) {
	var wg sync.WaitGroup
	wg.Add(len(urls))

	for _, url := range urls {
		go func(url string) {
			defer wg.Done()
			resp, err := http.Get(url)
			if err != nil {
				fmt.Printf("Error fetching %s: %v\n", url, err)
				return
			}
			defer resp.Body.Close()

			body, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				fmt.Printf("Error reading response body for %s: %v\n", url, err)
				return
			}

			// Process the response body as needed
			// For now, just print the length of the body
			fmt.Printf("Fetched %s, Body length: %d\n", url, len(body))
		}(url)
	}

	wg.Wait()
}

func main() {
	filePath := "data/05-tps-url.txt"

	// Read the file containing URLs
	urls, err := readLines(filePath)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		return
	}

	batchSize := 20
	for i := 0; i < len(urls); i += batchSize {
		end := i + batchSize
		if end > len(urls) {
			end = len(urls)
		}
		batch := urls[i:end]
		fmt.Printf("Fetching batch %d - %d\n", i+1, end)
		fetchData(batch)
		time.Sleep(1 * time.Second) // Optional: add a delay between batches
	}
}

func readLines(filePath string) ([]string, error) {
	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		return nil, err
	}
	lines := strings.Split(string(data), "\n")
	var result []string
	for _, line := range lines {
		if line != "" {
			result = append(result, line)
		}
	}
	return result, nil
}
