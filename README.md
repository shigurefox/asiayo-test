# Asiyao

## 題目一

```sql
SELECT
    orders.bnb_id,
    bnbs.name AS bnb_name,
    sum(orders.amount) AS may_amount
FROM
    orders
    LEFT JOIN bnbs ON orders.bnb_id = bnbs.id
WHERE
    orders.created_at BETWEEN '2023-05-01 00:00:00'::timestamp AND '2023-06-01 00:00:00'::timestamp
    AND orders.currency = 'TWD'
GROUP BY orders.bnb_id
ORDER BY may_amount DESC
LIMIT 10
```

## 題目二

假設問題是單純只有在資料庫中執行題目一的語句時發現執行速度很慢，那麼可以先嘗試對語句作優化

1. 檢查語句裡面 where, join 相關的表裡有沒有設 index，使用 explain, profiling 等功能查看是不是有用到 index
2. 檢查是否能減少 where 裡面子句的複雜度、避免過多 function call 或是運算
3. 檢查語句有沒有其實用不到的欄位

其次是依業務邏輯和系統資訊作檢查和判斷

1. 考量使用者的數量：
   是否同時有太多使用者會執行這個 query 導致查表變慢
   可以用 show process list 查看
   這部分的優化以減少 query 執行的次數為大方向
   例如如果語句是用在定期的報表資料拉取，看能不能用 cache 等方式，或是定期搬移資料做快照等
2. 從系統效能和監控工具查看是否有硬體面的效能瓶頸
3. 架構可行的話考慮用 partition 或 sharding 縮小語句的查詢範圍

## API doc

API 使用 Flask 框架做最小功能實作，說明文件詳見 `api.md`。

測試方法為在 terminal 執行 app.py 啟動 API server 後在另一個分頁執行 test.py。

----

## 經驗分享

1. SOLID 指 OOP 的五項基本原則，包含：

   1. 單一職責原則 (Single Responsibility Principle, SRP)：一個類別應該只有一個引起變化的原因。換句話說，一個類別應該只有一個職責。
   2. 開放封閉原則 (Open-Closed Principle, OCP)：軟體實體（類別、模組、函式等）應該對擴展是開放的，對修改是封閉的。這表示當需要新增功能時，應該擴展現有的程式碼，而不是修改它。
   3. 里氏替換原則 (Liskov Substitution Principle, LSP)：衍生類別應該能夠替換掉基礎類別，而不影響程式的正確性。換句話說，衍生類別應該能夠被當作基礎類別使用。
   4. 介面隔離原則 (Interface Segregation Principle, ISP)：不應該強迫類別實作它們不需要的介面。這有助於避免類別因為實作無用的方法而變得複雜。
   5. 依賴反轉原則 (Dependency Inversion Principle, DIP)：高階模組不應該依賴於低階模組，兩者都應該依賴於抽象。這有助於降低模組間的耦合度，增加程式碼的靈活性。

其中 ISP 指我們在定義介面時，應該要盡量分割成小而特定的部分，避免出現對某些類別不必要的方法。這樣有助於類別變得太龐雜，也比較容易依照需求來實作介面。
DIP 則指高階模組和低階模組都應該依賴於抽象，如介面或抽象類別。例如高階模組中某個部分需要做資料庫的存取，那麼我們應該定義一個抽象的資料庫介面，讓高階模組依賴這個抽象介面，再由低階模組來實作這個介面。兩者都有助於解決程式碼不易擴充的問題。

1. FP 與 OOP 的比較如下：

- FP 以函式來處理資料和執行運算，並強調避免狀態改變與可變資料。函式可以在其他函式間傳遞，或是嵌套在其他函式上。
- OOP 以物件來表示一個個資料和其對應的操作方法，強調程式的組成和建模。物件之間可以協作，繼承或是合成等方式來以開發者容易理解的形式達成複雜的功能。
- 兩種範式可以搭配使用，如在 Python 中函式也被視為一個物件，可以用 map, reduce 等高等函式對物件進行處理，而不需要自行定義迴圈和宣告區域變數。
- 類別可以視為產出一類物件的藍圖，實體則是依照類別定義製造出的產物，如定義出一個汽車類別後，我們可以製造出許多個汽車的物件實體，並且可以呼叫方法個別操控各個實體的行為。

3.  

- Interface 旨在實作類別前先規範好應該有哪些方法，以及參數、回傳型別等資訊。這有助於將程式模組化，增加可讀性和易維護性。
- OOP 的多型由繼承特性而來，指同樣的一個函式可以依據上下文參數的不同產生不同的行為。
- 例如在一個 Animal 的類別中，定義了一個發出叫聲的方法，假設有 Dog, Cat 兩個類別繼承自 Animal，那麼我們可以定義出一個包含發出叫聲這個方法的 interface，再在 Dog, Cat 類別中實作發出叫聲的方法。如此一來外部程式只需要知道 interface 的定義，在處理時便可自動依傳入的類別選用正確的方法。

4.  

- 一般而言我們會在 git 的提交歷史中看到哪些變更是提交到哪一個分支等資訊，在整合分支時我們可以根據想要的結果選用合適的方法
- git rebase 是其中一種合併分支的方法，例如 repo 中有個主分支 main 和實作某個功能的 feature 分支，在完成 feature 分支時，我們可以用 git rebase 在 main 分支後面套用來自 feature 分支的變更，最後讓這些變更看起來處在同一條線，就像是直接在 main 上提交的變更一樣。
- git merge 則會額外產生一個 merge commit，將兩個分支的 commit 整合在一起。
  fast-forward mode 發生在 main 分支從分岔出 feature 分支之後沒有其他變更的情況，此時在完成合併後會呈現一直線，如同將 feature 分支的變更直接提交到 main 的情況。
  non-fast-forward mode 則是發生在 main 分支有其他變更，或是希望保留 feature 分支原有的提交歷史，這時會產生額外的 merge commit 以解決兩分支的檔案衝突，並保留原有分支的提交歷史。
