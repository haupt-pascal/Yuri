package main

import (
	"crypto/sha256"
	"fmt"
	"log"
	"math/big"
	"math/rand"
	"time"
)

const (
	base58Alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
)

func generateAddress(key *big.Int) string {
	extendedKey := append([]byte{0x80}, key.Bytes()...)
	firstHash := sha256.Sum256(extendedKey)
	secondHash := sha256.Sum256(firstHash[:])
	checksum := secondHash[:4]
	finalKey := append(extendedKey, checksum...)
	return base58Encode(finalKey)
}

func base58Encode(input []byte) string {
	x := new(big.Int).SetBytes(input)
	base := big.NewInt(58)
	zero := big.NewInt(0)
	encoded := ""
	for x.Cmp(zero) > 0 {
		mod := new(big.Int)
		x.DivMod(x, base, mod)
		encoded = string(base58Alphabet[mod.Int64()]) + encoded
	}
	return encoded
}

func checkWallet(startKey, endKey *big.Int, targetWallet string) string {
	checkedKeys := big.NewInt(0)
	totalKeys := new(big.Int).Sub(endKey, startKey)
	startTime := time.Now()

	log.Printf("Checking keys from %s to %s...\n", startKey.Text(16), endKey.Text(16))

	rand.Seed(time.Now().UnixNano()) // Seed the random number generator

	for checkedKeys.Cmp(totalKeys) <= 0 {
		currentKey := new(big.Int).Rand(rand.New(rand.NewSource(time.Now().UnixNano())), totalKeys)
		currentKey.Add(currentKey, startKey)
		fmt.Println(currentKey.Text(16))
		address := generateAddress(currentKey)
		if address == targetWallet {
			elapsedTime := time.Since(startTime)
			keysPerSecond := new(big.Float).Quo(new(big.Float).SetInt(checkedKeys), new(big.Float).SetFloat64(elapsedTime.Seconds()))
			fmt.Printf("Average Keys per Second: %.2f\n", keysPerSecond)
			return fmt.Sprintf("Wallet gefunden! Schlüssel: %s, Adresse: %s\nDurchschnittliche Keys pro Sekunde: %s", currentKey.Text(16), address, keysPerSecond.Text('f', 2))
		}
		checkedKeys.Add(checkedKeys, big.NewInt(1))
	}

	elapsedTime := time.Since(startTime)
	keysPerSecond := new(big.Float).Quo(new(big.Float).SetInt(checkedKeys), new(big.Float).SetFloat64(elapsedTime.Seconds()))
	fmt.Printf("Average Keys per Second: %.2f\n", keysPerSecond)

	log.Println("Wallet not found in the defined range.")
	return "Wallet nicht gefunden im definierten Bereich."
}

func main() {
	startKey, _ := new(big.Int).SetString("2000000000000000", 16)
	endKey, _ := new(big.Int).SetString("3FFFFFFFFFFFFFFF", 16)
	targetWallet := "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"

	result := checkWallet(startKey, endKey, targetWallet)
	fmt.Println(result)

	// Wait for user input before exiting
	fmt.Println("Press Enter to exit...")
	fmt.Scanln()
}
