# 匯率轉換 API 參考文檔

## 描述

此 API 可用來進行匯率轉換，從一個貨幣轉換為另一個貨幣。

## 路徑

- `GET /api/v1/exchange`

## 參數

| 欄位      | 型別     | 必要參數 | 說明   | 範例 |
| --------- | -------- | -------- | ------ | ---- |
| `source`  | `string` | Y | 要轉換的原始貨幣代碼 | `USD` |
| `target`  | `string` | Y | 目標貨幣代碼 | `JPY` |
| `amount`  | `float` | Y | 要轉換的原始貨幣金額，可以包含千分位逗點 | `1,234.56` |
| `is_round` | `boolean` | N | 是否做四捨五入，預設為 `True` | `True` |

## 回傳格式

| 欄位      | 型別     | 說明   | 範例 |
| --------- | -------- | ------ | ---- |
| `source`  | `string` | 要轉換的原始貨幣代碼 | `USD` |
| `target`  | `string` | 目標貨幣代碼 | `JPY` |
| `amount`  | `float`  | 要轉換的原始貨幣金額，可以包含千分位逗點 | `1,525.00` |
| `converted_amount` | `boolean` | 轉換後的數字，包含千分位逗點 | `30,444.00` |
| `error` | `string` | 如轉換失敗，將回傳錯誤訊息 |  |

## 範例

### 請求

```sql
GET /api/v1/exchange?source=USD&target=TWD&amount=1,000
```

### 回傳結果

```json
{
    "source_currency": "USD",
    "target_currency": "TWD",
    "exchange_rate": 30.444,
    "amount": "1,000",
    "converted_amount": "30,444.00"
}
```

## 錯誤處理

- 如果缺少 source 或 target 參數，將返回 HTTP 400 錯誤。
- 如果無法將 amount 參數轉為數字，將返回 HTTP 400 錯誤並帶有對應的錯誤訊息。

## 注意事項

- 請確保提供的貨幣代碼和金額格式是正確的。
- 請注意數字格式，可以包含千分位逗點，但不應包含其他非數字字符。
