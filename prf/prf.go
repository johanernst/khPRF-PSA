package prf

import "fmt"
import "math/big"
import "strconv"

import "github.com/fentec-project/gofe/data"

import "golang.org/x/crypto/sha3"


/*
The Evaluate function in this file implements the key-homomorphic PRF $F(k,x) := \lfloor \langle H(x),k\rangle \rfloor_p$
It is mentioned in https://eprint.iacr.org/2015/220.pdf on page 2.
*/

//These variables are used to reduce the number of SHA3 calls. One call to SHA3 is used for several calls to hash(...).
var hash_index = 0
const max_hash_index = 64 //byte length of the output of the hash function.
const output_length = 16 //number of bytes used per call to Hash
var hash_value [max_hash_index]byte //array for storing the sha3_512 value

//This function implements the PRF
func Evaluate(input string, key data.Vector, key_mod *big.Int, message_mod *big.Int) (*big.Int, error) {
    result := big.NewInt(0)
    for i := 0; i < len(key); i++ {
        product := big.NewInt(0)
        integer_hash_value := hash(input, i)
        product.Mul(integer_hash_value, key[i])
        result.Add(result, product)
    }
    
    return_value, err := round(result, key_mod, message_mod)
    if err != nil {
        fmt.Println("Error in round function.")
    }
    return return_value, nil
}

// This returns fresh hash values. It calls sha3 whenever new values are needed.
func hash(input string, pos int) (*big.Int) {
    integer_hash_value := big.NewInt(0)
    if hash_index == 0 {
        hash_value = sha3.Sum512([]byte(strconv.Itoa(pos) + " " + input))
    }
    integer_hash_value.SetBytes(hash_value[hash_index:hash_index + output_length])
    hash_index = (hash_index + output_length) % max_hash_index
    
    return integer_hash_value
}

//This function implements $\lfloor value \rfloor_{lower_mod}$, that is the LWR rounding function.
func round(value, upper_mod, lower_mod *big.Int) (*big.Int, error) {
    if lower_mod.Cmp(upper_mod) >= 0 {
        return nil, fmt.Errorf("Illegal input to rounding function")
    }
    value.Mod(value, upper_mod)
    value.Mul(value, lower_mod)
    value.Div(value, upper_mod)
    
    return value, nil
}
