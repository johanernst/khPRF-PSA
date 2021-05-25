//psa_test.go
package psa

import (
    "testing"
    "fmt"
    "time"
    "os"
    "math/big"
    "strconv"
    "github.com/fentec-project/gofe/data"
	"github.com/fentec-project/gofe/sample"
)

const max_value int = 1000000000 //plaintexts are between 0 and this value

func TestRuntime(t *testing.T) {
    /*This memory will acutally never be allocated, because we never read or write to this memory,
     but it prevents the garbage collector from running too frequently
     and creating weir peaks in the running time. See e.g. 
     https://blog.twitch.tv/en/2019/04/10/go-memory-ballast-how-i-learnt-to-stop-worrying-and-love-the-heap-26c2462549a2/ 
     for reference. */
    ballast := make([]byte, 2<<32)
    _ = ballast
    
    num_clients, _ := strconv.Atoi(os.Args[4])
    clients := make([]*PSAClient, num_clients)
    ciphertexts := make([]*big.Int, num_clients)
    
    file, err := os.OpenFile("runtime.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        fmt.Println(err)
    }
    defer file.Close()

    start := time.Now()
    for i := 0; i < num_clients; i++ {
        new_client, err := NewPSAClient(i)
        
        if err != nil {
            fmt.Println(err)
        }
        clients[i] = new_client
    }
    //compute decryption key
    dec_key := data.NewConstantVector(Dimension, big.NewInt(0))
    for i := 0; i < num_clients; i++ {
      dec_key = dec_key.Add(clients[i].ClientEncKey)
    }
    dec_key = dec_key.Mod(key_mod)
    runtime_setup := time.Since(start)
    
    label := 0
    
    plaintexts, err := data.NewRandomVector(num_clients, sample.NewUniform(big.NewInt(int64(max_value))))
    if err != nil {
        fmt.Println(err)
    }
    
	time.Sleep(120 * time.Second)    //Let the processor cool down a bit
    
    runtime_enc := int64(0)
    for i := 0; i < num_clients; i++ {
        start = time.Now()
        ciphertexts[i], err = clients[i].Encrypt(plaintexts[i], strconv.Itoa(label), num_clients)
        dur := time.Since(start)

        if err != nil {
            fmt.Println(err)
        }
        runtime_enc += dur.Nanoseconds()
    }
    
    sum_plaintexts := big.NewInt(0)
    for i := 0; i < num_clients; i++ {
        sum_plaintexts.Add(sum_plaintexts, plaintexts[i])
    }

    runtime_dec := int64(0)
    dec_value := big.NewInt(0)
    for i := 0; i < 1000; i++ {
        start = time.Now()
        dec_value, err = PSADecrypt(ciphertexts, dec_key, strconv.Itoa(label), num_clients)
        dur := time.Since(start)
        runtime_dec += dur.Nanoseconds()
        if err != nil {
            fmt.Println(err)
        }
    }
    
    fmt.Printf("Decrypted value:   %v\nSum of plaintexts: %v\n", dec_value, sum_plaintexts)
    if dec_value.Cmp(sum_plaintexts) != 0 {
        fmt.Println("ALERT: decryption != sum of plaintexts")
        fmt.Println(dec_value)
        fmt.Println(sum_plaintexts)
    }
    
    fmt.Println("total encrytion (nano sec.):", int64(runtime_enc))
	fmt.Println("total decrytion (nano sec.):", int64(runtime_dec))
	
	_, err3 := file.WriteString(fmt.Sprintf("%d;%d;%d;%d\n", num_clients, runtime_enc, runtime_dec, runtime_setup))   //qqq
    if err3 != nil {
        fmt.Println(err)
    }
}
