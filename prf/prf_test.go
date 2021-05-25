package prf

import "testing"
import "fmt"
import "math/big"

import "golang.org/x/crypto/sha3"

import "github.com/fentec-project/gofe/data"

//Test whether the PRF with a fixed key outputs the correct value. "correct" here means: same value as in a previous version.
func TestGetVal(t *testing.T) {
    fmt.Println("Starting prf test")

    const dimension = 2048
    var message_mod *big.Int = new(big.Int).Exp(big.NewInt(2), big.NewInt(84) ,nil)
    var key_mod *big.Int = new(big.Int).Exp(big.NewInt(2), big.NewInt(128) ,nil)
    seed := sha3.Sum256(big.NewInt(46235981483589).Bytes())

    prf_key, err := data.NewRandomDetVector(dimension, key_mod, &seed)
    if err != nil {
        t.Error("NewRandomDetVector returned error")
    }
    
    prf_value, err2 := Evaluate("0", prf_key, key_mod, message_mod)
    if err2 != nil {
        t.Error("prf.Evaluate returned error")
    }
    
    fmt.Println(prf_value)
    expected_result := big.NewInt(1).Mul(big.NewInt(1410145845266814), big.NewInt(10000000000))
    expected_result.Add(expected_result, big.NewInt(1302685721))
    
    if prf_value.Cmp(expected_result) != 0 {
        t.Error("prf value was incorrect")
    }
}
