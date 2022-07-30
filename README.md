# Projects

## 小组成员及对应 GitHub 账号

| 姓名 | 学号 | GitHub 账号 |
| --- | --- | --- |
| 李岱耕 | 202000460088 | [Jemtaly](https://github.com/Jemtaly) |
| 郭灿林 | 202000460092 | [Fix3dP0int](https://github.com/Fix3dP0int) |
| 李婕 | 202020141138 | [ytbi](https://github.com/ytbi) |

## 成员分工

| 项目目录 | 贡献者 |
| --- | --- |
| [SM3](SM3) | 李岱耕 |
| [SM3bygcl](SM3bygcl) | 郭灿林 |
| [Bitcoin](Bitcoin) | 郭灿林 |
| [Ethereum](Ethereum) | 郭灿林 |
| [SM2](SM2) | 李岱耕 |
| [SM2bygcl](SM2bygcl) | 郭灿林 |
| [Real world cryptanalyses](Real%20world%20cryptanalyses) | 李婕 |
| [Real world zk](Real%20world%20zk) | 李婕 |

## 项目清单

- SM3
    - [x] Project: implement the naïve birthday attack of reduced SM3
    - [x] Project: implement the Rho method of reduced SM3
    - [x] Project: implement length extension attack for SM3, SHA256, etc.
    - [x] Project: do your best to optimize SM3 implementation (software)
    - [x] Project: Impl Merkle Tree following RFC6962
    - [ ] Project: Try to Implement this scheme

- SM2
    - [ ] Project: report on the application of this deduce technique in Ethereum with ECDSA
    - [x] Project: impl sm2 with RFC6979
    - [x] Project: verify the above pitfalls with proof-of-concept code
    - [ ] Project: Implement the above ECMH scheme
    - [x] Project: Implement a PGP scheme with SM2
    - [ ] Project: implement sm2 2P sign with real network communication
    - [ ] Project: PoC impl of the scheme, or do implement analysis by Google
    - [ ] Project: implement sm2 2P decrypt with real network communication

- Bitcoin
    - [x] Project: forge a signature to pretend that you are Satoshi

- Bitcoin-public
    - [ ] Project: send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself
    - [x] Project: forge a signature to pretend that you are Satoshi

- Eth-public
    - [x] Project: research report on MP

- Real world cryptanalyses
    - [x] Project: Find a key with hash value `sdu_cst_20220610` under a message composed of your name followed by your student ID. For example, `San Zhan 202000460001`.
    - [x] Project: Find a 64-byte message under some $k$ fulfilling that their hash value is symmetrical
 
- Real world zk
    - [ ] Project: Write a circuit to prove that your CET6 grade is larger than 425. a. Your grade info is like (cn_id, grade, year, sig_by_moe). These grades are published as commitments onchain by MoE. b. When you got an interview from an employer, you can prove to them that you have passed the exam without letting them know the exact grade. 
    - [ ] Project: The commitment scheme used by MoE is SHA256-based. a. commit = SHA256(cn_id, grade, year, sig_by_moe, r)
