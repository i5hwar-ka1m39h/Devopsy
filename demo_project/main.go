package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

type HealthResp struct {
	Status  string    `json:"status"`
	Uptime  time.Time `json:"uptime"`
	Message string    `json:"message"`
}

func main() {
	http.HandleFunc("/", getHtml)
	http.HandleFunc("/health", getHealth)

	fmt.Println("the server is running 5002")

	err := http.ListenAndServe(":5002", nil)

	if err != nil {
		fmt.Println("error from server", err)
		return
	}

}

func getHealth(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Content-Type", "application/json")

	resp := HealthResp{
		Status:  "OK",
		Uptime:  time.Now(),
		Message: "server is healty",
	}

	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(resp); err != nil {
		log.Println("error is  health resp encoding", err)
		return
	}

}

func getHtml(w http.ResponseWriter, r *http.Request) {

	http.ServeFile(w, r, "./index.html")
}
