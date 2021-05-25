package psa

import (
	"fmt"
	"math/big"

	"github.com/fentec-project/gofe/data"
	"github.com/fentec-project/gofe/sample"
	
	"github.com/johanernst/khPRF-PSA/prf"
)

type PSAClient struct {
    Idx int
    ClientEncKey data.Vector
}

/*
In LWR papers key_mod is usually denoted by q and message_mod by p and the
rounding function rounds from Z_q to Z_p.
Changing these values may break the implementation, because the implementation
of the PRF relies on the fact that 512 bit can be split into 4 (128 bit) values of Z_q.
*/
var message_mod *big.Int = new(big.Int).Exp(big.NewInt(2), big.NewInt(85) ,nil)
var key_mod *big.Int = new(big.Int).Exp(big.NewInt(2), big.NewInt(128) ,nil)
const Dimension int = 2096


//This function creates and returns a new client
func NewPSAClient(idx int) (*PSAClient, error) {
	prf_sampler := sample.NewUniform(key_mod)
	
	//create encryption key
	ek, err := data.NewRandomVector(Dimension, prf_sampler)
	if err != nil {
		return nil, fmt.Errorf("could not generate encryption key")
	}

	return &PSAClient{
		Idx:          idx,
		ClientEncKey: ek,
	}, nil
}

//This function encrypts the message x with the key of client c.
func (c *PSAClient) Encrypt(x *big.Int, label string, num_users int) (*big.Int, error) {
    prf_value, err := prf.Evaluate(label, c.ClientEncKey, key_mod, message_mod)
    if err != nil {
        fmt.Println(err)
        return nil, err
    }
    
    x_new, err := preprocessing(x, num_users)
    if err != nil {
        return nil, err
    }
    
    ciphertext := new(big.Int).Add(prf_value, x_new)
    ciphertext.Mod(ciphertext, message_mod)
    return ciphertext, nil
}

//This function takes as input the ciphertexts from all clients and outputs the sum of the plaintexts.
func PSADecrypt(ciphers []*big.Int, dec_key data.Vector, label string, num_clients int) (*big.Int, error) {
    sum := big.NewInt(0)
    
    for i := 0; i < len(ciphers); i++ {
        sum.Add(sum, ciphers[i])
    }
    
    prf_value, err := prf.Evaluate(label, dec_key, key_mod, message_mod)
    
    if err != nil {
        return nil, err
    }
    
    sum.Sub(sum, prf_value)
    sum.Mod(sum, message_mod)
    
    sum, err = postprocessing(sum, num_clients)
    if err != nil {
        return nil, err
    }
    sum.Mod(sum, message_mod)

    return sum, nil
}

//This function must be called before the actual encryption, because the PRF is only *almost* key-homomorphic
//x is the plaintext. The return value is what will then be input to the actual encryption
func preprocessing(x *big.Int, n int) (*big.Int, error) {
    result := big.NewInt(0)
    result.Mul(x, big.NewInt(int64(n)))
    result.Add(result, big.NewInt(1))
    
    if result.Cmp(message_mod) >= 0 {
        return nil, fmt.Errorf("Result = %v >= %v = message_mod", result, message_mod)
    }
    return result, nil
}

//This function must be called after decryption, to accomodate for the only *almost* key-homomorphism
//x is the output of the actual decryption. The return value is the sum of the plaintexts
func postprocessing(x *big.Int, n int) (*big.Int, error) {
    result := big.NewInt(0)
    remainder := big.NewInt(0)
    remainder.Mod(x, big.NewInt(int64(n)))
    if remainder.Cmp(big.NewInt(0)) == 0 {
        result = x
    } else {
        result.Add(x, big.NewInt(int64(n)))
        result.Sub(result, remainder)
    }
    
    result.Sub(result, big.NewInt(int64(n)))
    result.Div(result, big.NewInt(int64(n)))
    return result, nil
}
