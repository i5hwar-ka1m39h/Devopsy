FROM golang:1.25-alpine AS builder


WORKDIR /app

COPY go.mod ./ 
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o /go-server .

FROM scratch

WORKDIR /app

COPY --from=builder /go-server /app/go-server
COPY --from=builder /app/index.html /app/index.html

EXPOSE 5002


ENTRYPOINT ["/app/go-server"]
