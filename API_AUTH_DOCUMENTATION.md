# API de Autenticación - Laboratorio Esperanza

## Endpoints Disponibles

### 1. Login de Usuarios
**POST** `/api/auth/login`

Permite a los usuarios iniciar sesión en el sistema.

**Request Body:**
```json
{
  "username": "admin",
  "password": "Admin123!"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@labesperanza.com",
      "first_name": "Administrador",
      "last_name": "Sistema",
      "phone": "+51999999999",
      "role": "admin",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Response (401):**
```json
{
  "success": false,
  "message": "Credenciales incorrectas"
}
```

### 2. Registro de Usuarios (Solo Administradores)
**POST** `/api/auth/register`

Permite a los administradores registrar nuevos usuarios.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "username": "secretaria1",
  "email": "secretaria1@labesperanza.com",
  "password": "Secret123!",
  "first_name": "María",
  "last_name": "González",
  "phone": "+51987654321",
  "role": "secretary"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "data": {
    "id": 2,
    "username": "secretaria1",
    "email": "secretaria1@labesperanza.com",
    "first_name": "María",
    "last_name": "González",
    "phone": "+51987654321",
    "role": "secretary",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

### 3. Verificar Token
**POST** `/api/auth/verify`

Verifica si un token JWT es válido.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Token válido",
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@labesperanza.com",
      "first_name": "Administrador",
      "last_name": "Sistema",
      "role": "admin",
      "is_active": true
    }
  }
}
```

### 4. Obtener Perfil
**GET** `/api/auth/profile`

Obtiene el perfil del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@labesperanza.com",
    "first_name": "Administrador",
    "last_name": "Sistema",
    "phone": "+51999999999",
    "role": "admin",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

### 5. Actualizar Perfil
**PUT** `/api/auth/profile`

Actualiza el perfil del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "+51987654321",
  "email": "juan.perez@labesperanza.com"
}
```

### 6. Obtener Roles Disponibles
**GET** `/api/auth/roles`

Obtiene la lista de roles disponibles en el sistema.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "roles": ["admin", "secretary", "doctor", "technician"],
  "descriptions": {
    "admin": "Administrador - Acceso completo al sistema",
    "secretary": "Secretaria - Ingreso de resultados de laboratorio",
    "doctor": "Médico - Visualización de resultados",
    "technician": "Técnico - Procesamiento de muestras"
  }
}
```

### 7. Logout
**POST** `/api/auth/logout`

Cierra la sesión del usuario.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente"
}
```

## Roles y Permisos

### Roles Disponibles:
- **admin**: Acceso completo al sistema, puede crear usuarios
- **secretary**: Puede ingresar resultados de laboratorio
- **doctor**: Puede visualizar resultados de laboratorio
- **technician**: Puede procesar muestras

### Middleware de Autorización:
- `@token_required`: Requiere autenticación
- `@admin_required`: Requiere rol de administrador
- `@secretary_required`: Requiere rol de secretaria
- `@doctor_required`: Requiere rol de médico
- `@technician_required`: Requiere rol de técnico
- `@admin_or_secretary_required`: Requiere rol de admin o secretaria
- `@medical_staff_required`: Requiere rol médico (doctor o technician)

## Validaciones de Contraseña

Las contraseñas deben cumplir con los siguientes requisitos:
- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos una letra minúscula
- Al menos un número
- Al menos un carácter especial (!@#$%^&*(),.?":{}|<>)

## Códigos de Error Comunes

- **400**: Bad Request - Datos inválidos o faltantes
- **401**: Unauthorized - Token inválido o credenciales incorrectas
- **403**: Forbidden - Sin permisos para realizar la acción
- **404**: Not Found - Recurso no encontrado
- **500**: Internal Server Error - Error interno del servidor

## Ejemplo de Uso en Frontend

```javascript
// Login
const login = async (username, password) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Guardar token en localStorage
    localStorage.setItem('token', data.data.token);
    localStorage.setItem('user', JSON.stringify(data.data.user));
    
    // Redireccionar según rol
    switch (data.data.user.role) {
      case 'admin':
        window.location.href = '/admin-dashboard';
        break;
      case 'secretary':
        window.location.href = '/secretary-dashboard';
        break;
      case 'doctor':
        window.location.href = '/doctor-dashboard';
        break;
      case 'technician':
        window.location.href = '/technician-dashboard';
        break;
    }
  }
  
  return data;
};

// Verificar token
const verifyToken = async () => {
  const token = localStorage.getItem('token');
  if (!token) return false;
  
  const response = await fetch('/api/auth/verify', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  return data.success;
};

// Logout
const logout = async () => {
  const token = localStorage.getItem('token');
  
  await fetch('/api/auth/logout', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  // Limpiar localStorage
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  
  // Redireccionar a login
  window.location.href = '/login';
};
```




























