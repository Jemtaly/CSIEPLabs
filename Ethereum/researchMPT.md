# MPT源码分析

本报告主要参考以下两篇博文写成，大多数是引用博文中的内容，跟着两篇文章过了一遍。

[1] https://blog.csdn.net/lj900911/article/details/84981395?spm=1001.2014.3001.5502

[2] https://blog.csdn.net/qq_50665031/article/details/123555027

## Node节点

有四种node接口，分别为`fullNode`,`shortNode`,`valueNode`,`hashNode`，其中`fullNode`为分支节点，可以有多个子节点，`shortNode`为扩展节点，只有一个子节点，`valueNode`为叶子节点，`hashNode`是`fullNode`和`shortNode`对象的RLP哈希值，没有子节点。

从下面代码可以看到，`fullNode`有17个元素，其中16个表示`0-F`16个节点，第17位是`fullNode`本身的数据，`shortNode`中的`Val`指向下一个节点，它的特点是把多个只有一个子节点的父节点和其子节点合并起来从而缩短了树的深度，`valueNode`保存数据的结点，存储hash值，`hashNode`为`fullNode`或`shortNode`对象的RLP哈希值，被两者间接持有，就是两个结构体中的`nodeFlag`。

```GO
type node interface {
	fstring(string) string
	cache() (hashNode, bool)
	canUnload(cachegen, cachelimit uint16) bool
}
 
type (
	fullNode struct {
		Children [17]node // Actual trie node data to encode/decode (needs custom encoder)
		flags    nodeFlag
	}
	shortNode struct {
		Key   []byte
		Val   node
		flags nodeFlag
	}
	hashNode  []byte
	valueNode []byte
)
```

## 结构定义

Trie的定义在`trie.go`文件中找到。

```GO
type Trie struct {
   db   *Database
   root node
   cachegen, cachelimit uint16
}
```

其中`root`表示MPT的根节点，`db`是后端的KV存储，trie的结构最终都需要通过KV的形式存储到数据库，启动时需要从数据库加载。`cachegen`表示当前trie树的cache的generation values，每次commit操作cachegen都是增1，同时node会更新，默认是`node.nodeFlag.gen = cachegen`，如果`gen`小于`cachegen`且`cachegen - cachelimit`大于`gen`，意味着`trie commit`之后，`node`没有更新，那么`node`会从cache里面卸载，以节约内存，即cache的LRU算法。

## Trie的初始化

Trie调用`New`函数来初始化，参数分别有`root`和`db`，其中`root`是一个hash值，若`root`非空，则从数据库汇中加载一个已经存在的Trie，调用`resolveHash`方法根据给的参数`root`找到Trie。

```GO
// New creates a trie with an existing root node from db.
//
// If root is the zero hash or the sha3 hash of an empty string, the
// trie is initially empty and does not require a database. Otherwise,
// New will panic if db is nil and returns a MissingNodeError if root does
// not exist in the database. Accessing the trie loads nodes from db on demand.
func New(root common.Hash, db *Database) (*Trie, error) {
	if db == nil {
		panic("trie.New called without a database")
	}
	trie := &Trie{
		db: db,
	}
	if root != (common.Hash{}) && root != emptyRoot {
		rootnode, err := trie.resolveHash(root[:], nil)
		if err != nil {
			return nil, err
		}
		trie.root = rootnode
	}
	return trie, nil
}
```

`resolveHash()`方法是通过hash解析出node的RLP值。

```GO
func (t *Trie) resolveHash(n hashNode, prefix []byte) (node, error) {
    cacheMissCounter.Inc(1)
 
    hash := common.BytesToHash(n)
    //通过hash解析出node的RLP值
    enc, err := t.db.Node(hash)
    if err != nil || enc == nil {
        return nil, &MissingNodeError{NodeHash: hash, Path: prefix}
    }
    return mustDecodeNode(n, enc, t.cachegen), nil
}
```

## Trie的插入和查找

### 插入

Trie的插入使用函数`insert`，使用的是递归的方法寻找到可以插入的点进行插入，参数`node`是要插入的节点，`prefix`是每个子过程已经处理完的部分key，参数`key`和`prefix`互补，是未处理的部分key，`value`是要插入的值，插入函数返回bool类型，表示是否改变了trie树，`node`是插入完成后的子树的根节点。

基本流程如下:

1. 如果节点类型是`nil`，此时树是空的，直接返回`shortNode{key, value, t.newFlag()}`类型，树就只含有一个`shortNode`叶子节点。
2. 如果当前节点类型是`shortNode`
   - 计算公共前缀，若公共前缀等于key，那么说明这两个key是相等的，如果value也相等，即`dirty==false`，那么返回错误；
   - 如果没有错误就更新shortNode的值并返回。如果公共前缀不完全匹配，就需要把公共前缀提取出来形成一个独立的结点（扩展节点），扩展结点连接一个branch节点，branch节点的定义为`branch := &fullNode{flags: t.newFlag()}`，branch节点后面连接两个shortNode节点，它的子节点位置调用`t.insert`插入剩下的两个shortNode节点。
3. 如果当前节点类型是`fullNode`，那么直接在对应的子节点调用`insert`方法，把对应的子节点指向新生成的节点。
4. 如果当前节点类型是`hashNode`，表示当前节点还没加载到内存里，还存放在数据库里，首先需要调用`t.resolveHash(n, prefix)`加载到内存，生成节点后再调用`insert`方法插入。


```GO
func (t *Trie) insert(n node, prefix, key []byte, value node) (bool, node, error) {

   //key要求非空
   if len(key) == 0 {
      if v, ok := n.(valueNode); ok {
         return !bytes.Equal(v, value.(valueNode)), value, nil
      }
      return true, value, nil
   }

   switch n := n.(type) {

   case *shortNode:
      matchlen := prefixLen(key, n.Key)
      //如果整个键匹配，则保持这个短节点不变
      // 并且只更新值。
      if matchlen == len(n.Key) {
         dirty, nn, err := t.insert(n.Val, append(prefix, key[:matchlen]...), key[matchlen:], value)
         if !dirty || err != nil {
            return false, n, err
         }
         //如果没有错误就更新shortNode的值然后返回。
         return true, &shortNode{n.Key, nn, t.newFlag()}, nil
      }

      branch := &fullNode{flags: t.newFlag()}
      var err error
      //然后再branch节点的Children位置调用t.insert插入剩下的两个short节点。
      _, branch.Children[n.Key[matchlen]], err = t.insert(nil, append(prefix, n.Key[:matchlen+1]...), n.Key[matchlen+1:], n.Val)
      if err != nil {
         return false, nil, err
      }
      _, branch.Children[key[matchlen]], err = t.insert(nil, append(prefix, key[:matchlen+1]...), key[matchlen+1:], value)
      if err != nil {
         return false, nil, err
      }
      // 如果这个shortnode出现在索引0处，则用分支替换它。
      if matchlen == 0 {
         return true, branch, nil
      }
      // 否则，将其替换为一个通向分支的短节点。
      return true, &shortNode{key[:matchlen], branch, t.newFlag()}, nil

   case *fullNode:
      //如果当前的节点是fullNode(也就是branch节点)，
      //那么直接往对应的孩子节点调用insert方法,然后把对应的孩子节点只想新生成的节点。
      dirty, nn, err := t.insert(n.Children[key[0]], append(prefix, key[0]), key[1:], value)
      if !dirty || err != nil {
         return false, n, err
      }
      n = n.copy()
      n.flags = t.newFlag()
      n.Children[key[0]] = nn
      return true, n, nil

   case nil:
      return true, &shortNode{key, value, t.newFlag()}, nil

   case hashNode:
      //如果当前节点是hashNode, hashNode的意思是当前节点还没有加载到内存里面来，
      //还是存放在数据库里面，那么首先调用 t.resolveHash(n, prefix)来加载到内存，
      //然后对加载出来的节点调用insert方法来进行插入。
      rn, err := t.resolveHash(n, prefix)
      if err != nil {
         return false, nil, err
      }
      dirty, nn, err := t.insert(rn, prefix, key, value)
      if !dirty || err != nil {
         return false, rn, err
      }
      return true, nn, nil

   default:
      panic(fmt.Sprintf("%T: invalid node: %v", n, n))
   }
}

```

## 查找

Trie树的查找使用`Get`方法，主要是通过遍历Trie树来获取`Key`对应的`value`。

```Go
func (t *Trie) tryGet(origNode node, key []byte, pos int) (value []byte, newnode node, didResolve bool, err error) {
	switch n := (origNode).(type) {
	case nil:
		return nil, nil, false, nil
	case valueNode:
		return n, n, false, nil
	case *shortNode:
		if len(key)-pos < len(n.Key) || !bytes.Equal(n.Key, key[pos:pos+len(n.Key)]) {
			// key not found in trie
			return nil, n, false, nil
		}
		value, newnode, didResolve, err = t.tryGet(n.Val, key, pos+len(n.Key))
		if err == nil && didResolve {
			n = n.copy()
			n.Val = newnode
			n.flags.gen = t.cachegen
		}
		return value, n, didResolve, err
	case *fullNode:
		value, newnode, didResolve, err = t.tryGet(n.Children[key[pos]], key, pos+1)
		if err == nil && didResolve {
			n = n.copy()
			n.flags.gen = t.cachegen
			n.Children[key[pos]] = newnode
		}
		return value, n, didResolve, err
	case hashNode:
		child, err := t.resolveHash(n, key[:pos])
		if err != nil {
			return nil, n, true, err
		}
		value, newnode, _, err := t.tryGet(child, key, pos)
		return value, newnode, true, err
	default:
		panic(fmt.Sprintf("%T: invalid node: %v", origNode, origNode))
	}
}
```

## KEY加密

在security_trie.go中定义了`SecureTrie`对trie树进行了包装，所有的key都转换成keccak256算法计算的hash值，用`secKeyCache`存储hash值和key的映射。

```Go
type SecureTrie struct {
   trie             Trie//原始的Trie树
   hashKeyBuf       [common.HashLength]byte//计算hash值的buf
   secKeyCache      map[string][]byte//记录hash值和对应的key的映射
   secKeyCacheOwner *SecureTrie // Pointer to self, replace the key cache on mismatch
}
```

Commit函数将所有节点和对应的安全哈希写入到trie的数据库，节点以其sha3哈希值作为密钥存储，commit将从内存中刷新节点。

```Go
func (t *SecureTrie) Commit(onleaf LeafCallback) (common.Hash, int, error) {
	// Write all the pre-images to the actual disk database
	if len(t.getSecKeyCache()) > 0 {
		if t.trie.db.preimages != nil { // Ugly direct check but avoids the below write lock
			t.trie.db.lock.Lock()
			for hk, key := range t.secKeyCache {
				t.trie.db.insertPreimage(common.BytesToHash([]byte(hk)), key)
			}
			t.trie.db.lock.Unlock()
		}
		t.secKeyCache = make(map[string][]byte)
	}
	// Commit the trie to its intermediate node database
	return t.trie.Commit(onleaf)
}
```
