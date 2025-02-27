# Pixel jumper docs

## Supported requests:

#### Note: "error_type" field will occur only when status is "ERROR"

### 1. **POST** `/create-user`
#### **Body:**
```json
{
  "login": "<str>",
  "password": "<str>"
}
```
#### **Response:**
```json
{
  "status": "<SUCCESS | ERROR>",
  "error_type": "<USERNAME_TOO_SHORT | PASSWORD_TO_SHORT | ACCOUNT_ALREADY_EXISTS>"
}
```

---

### 2. **PUT** `/provide-result`
#### **Body:**
```json
{
  "login": "<str>",
  "score": "<int>"
}
```
#### **Response:**
```json
{
  "status": "<SUCCESS | ERROR>",
  "error_type": "<WRONG_FORMAT | ACCOUNT_DO_NOT_EXIST>"
}
```

---

### 3. **PUT** `/change-password`
#### **Body:**
```json
{
  "login": "<str>",
  "password": "<str>",
  "new_password": "<str>"
}
```
#### **Response:**
```json
{
  "status": "<SUCCESS | ERROR>",
  "error_type": "<ACCOUNT_DO_NOT_EXIST | PASSWORD_TOO_WEAK | WRONG_PASSWORD | PASSWORD_NOT_CHANGED>"
}
```

---

### 4. **GET** `/login`
#### **Body:**
```json
{
  "login": "<str>",
  "password": "<str>"
}
```
#### **Response:**
```json
{
  "status": "<SUCCESS | ERROR>",
  "level": "<double>",
  "high_score": "<int>",
  "error_type": "<ACCOUNT_DO_NOT_EXIST | WRONG_PASSWORD>"
}
```

---

### 5. **DELETE** `/delete-user`
#### **Body:**
```json
{
  "login": "<str>",
  "password": "<str>"
}
```
#### **Response:**
```json
{
  "status": "<SUCCESS | ERROR>",
  "error_type": "<ACCOUNT_DO_NOT_EXIST | INCORRECT_CREDENTIALS>"
}
```