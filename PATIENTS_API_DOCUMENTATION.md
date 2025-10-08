# API de Pacientes - Laboratorio Esperanza

## Descripción
La API de pacientes permite gestionar la información completa de los pacientes del laboratorio, incluyendo datos personales, médicos, de contacto y seguros.

## Endpoints Disponibles

### 1. Crear Paciente
**POST** `/api/patients`

Crea un nuevo paciente en el sistema.

#### Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### Body (JSON)
```json
{
  "first_name": "Juan Carlos",
  "last_name": "Pérez García",
  "middle_name": "Antonio",
  "dpi": "1234567890123",
  "email": "juan.perez@email.com",
  "phone": "5555-1234",
  "phone_secondary": "5555-5678",
  "date_of_birth": "1990-05-15",
  "gender": "masculino",
  "marital_status": "soltero",
  "occupation": "Ingeniero",
  "nationality": "Guatemalteco",
  "address": "Zona 10, Ciudad de Guatemala",
  "city": "Guatemala",
  "department": "Guatemala",
  "postal_code": "01010",
  "blood_type": "O+",
  "allergies": "Ninguna conocida",
  "medical_history": "Sin antecedentes médicos relevantes",
  "current_medications": "Ninguna",
  "chronic_conditions": "Ninguna",
  "emergency_contact_name": "María García",
  "emergency_contact_phone": "5555-9999",
  "emergency_contact_relationship": "madre",
  "insurance_company": "Seguro Social",
  "insurance_policy_number": "SS-123456",
  "insurance_phone": "5555-0000",
  "notes": "Paciente de prueba para el sistema"
}
```

#### Campos Requeridos
- `first_name`: Nombre del paciente
- `last_name`: Apellido del paciente

#### Campos Opcionales
- `middle_name`: Segundo nombre
- `dpi`: Documento Personal de Identificación (único)
- `email`: Correo electrónico
- `phone`: Teléfono principal
- `phone_secondary`: Teléfono secundario
- `date_of_birth`: Fecha de nacimiento (YYYY-MM-DD)
- `gender`: Género (masculino, femenino, otro)
- `marital_status`: Estado civil (soltero, casado, divorciado, viudo)
- `occupation`: Ocupación
- `nationality`: Nacionalidad (default: Guatemalteco)
- `address`: Dirección
- `city`: Ciudad
- `department`: Departamento/Estado
- `postal_code`: Código postal
- `blood_type`: Tipo de sangre (A+, A-, B+, B-, AB+, AB-, O+, O-)
- `allergies`: Alergias conocidas
- `medical_history`: Antecedentes médicos
- `current_medications`: Medicamentos actuales
- `chronic_conditions`: Condiciones crónicas
- `emergency_contact_name`: Nombre del contacto de emergencia
- `emergency_contact_phone`: Teléfono del contacto de emergencia
- `emergency_contact_relationship`: Relación con el contacto de emergencia
- `insurance_company`: Compañía de seguros
- `insurance_policy_number`: Número de póliza
- `insurance_phone`: Teléfono del seguro
- `notes`: Notas adicionales

#### Respuesta Exitosa (201)
```json
{
  "success": true,
  "message": "Paciente creado exitosamente",
  "data": {
    "id": 1,
    "patient_code": "P20241215123",
    "dpi": "1234567890123",
    "first_name": "Juan Carlos",
    "last_name": "Pérez García",
    "middle_name": "Antonio",
    "full_name": "Juan Carlos Antonio Pérez García",
    "email": "juan.perez@email.com",
    "phone": "5555-1234",
    "phone_secondary": "5555-5678",
    "date_of_birth": "1990-05-15",
    "age": 34,
    "gender": "masculino",
    "marital_status": "soltero",
    "occupation": "Ingeniero",
    "nationality": "Guatemalteco",
    "address": "Zona 10, Ciudad de Guatemala",
    "city": "Guatemala",
    "department": "Guatemala",
    "postal_code": "01010",
    "blood_type": "O+",
    "allergies": "Ninguna conocida",
    "medical_history": "Sin antecedentes médicos relevantes",
    "current_medications": "Ninguna",
    "chronic_conditions": "Ninguna",
    "emergency_contact_name": "María García",
    "emergency_contact_phone": "5555-9999",
    "emergency_contact_relationship": "madre",
    "insurance_company": "Seguro Social",
    "insurance_policy_number": "SS-123456",
    "insurance_phone": "5555-0000",
    "notes": "Paciente de prueba para el sistema",
    "profile_image_url": null,
    "is_active": true,
    "created_at": "2024-12-15T10:30:00",
    "updated_at": "2024-12-15T10:30:00",
    "created_by": 1
  }
}
```

### 2. Obtener Paciente por ID
**GET** `/api/patients/{id}`

Obtiene la información completa de un paciente por su ID.

#### Headers
```
Authorization: Bearer <token>
```

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "data": {
    // Información completa del paciente
  }
}
```

### 3. Obtener Paciente por Código
**GET** `/api/patients/code/{patient_code}`

Obtiene la información completa de un paciente por su código único.

#### Headers
```
Authorization: Bearer <token>
```

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "data": {
    // Información completa del paciente
  }
}
```

### 4. Obtener Paciente por DPI
**GET** `/api/patients/dpi/{dpi}`

Obtiene la información completa de un paciente por su DPI.

#### Headers
```
Authorization: Bearer <token>
```

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "data": {
    // Información completa del paciente
  }
}
```

### 5. Buscar Pacientes
**GET** `/api/patients/search?q={search_term}&limit={limit}`

Busca pacientes por nombre, apellido, código o DPI.

#### Headers
```
Authorization: Bearer <token>
```

#### Parámetros de Query
- `q`: Término de búsqueda (requerido)
- `limit`: Límite de resultados (opcional, default: 50, máximo: 100)

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "patient_code": "P20241215123",
      "dpi": "1234567890123",
      "full_name": "Juan Carlos Antonio Pérez García",
      "phone": "5555-1234",
      "email": "juan.perez@email.com",
      "date_of_birth": "1990-05-15",
      "age": 34,
      "gender": "masculino",
      "is_active": true
    }
  ],
  "total": 1
}
```

### 6. Obtener Todos los Pacientes
**GET** `/api/patients?page={page}&per_page={per_page}&active_only={active_only}`

Obtiene todos los pacientes con paginación.

#### Headers
```
Authorization: Bearer <token>
```

#### Parámetros de Query
- `page`: Número de página (opcional, default: 1)
- `per_page`: Elementos por página (opcional, default: 20, máximo: 100)
- `active_only`: Solo pacientes activos (opcional, default: true)

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "patient_code": "P20241215123",
      "dpi": "1234567890123",
      "full_name": "Juan Carlos Antonio Pérez García",
      "phone": "5555-1234",
      "email": "juan.perez@email.com",
      "date_of_birth": "1990-05-15",
      "age": 34,
      "gender": "masculino",
      "is_active": true
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 1,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### 7. Actualizar Paciente
**PUT** `/api/patients/{id}`

Actualiza la información de un paciente existente.

#### Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

#### Body (JSON)
```json
{
  "phone": "5555-9999",
  "address": "Zona 15, Ciudad de Guatemala",
  "notes": "Paciente actualizado - información de contacto modificada"
}
```

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "message": "Paciente actualizado exitosamente",
  "data": {
    // Información actualizada del paciente
  }
}
```

### 8. Desactivar Paciente
**DELETE** `/api/patients/{id}`

Desactiva un paciente (soft delete).

#### Headers
```
Authorization: Bearer <token>
```

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "message": "Paciente desactivado exitosamente"
}
```

### 9. Reactivar Paciente
**POST** `/api/patients/{id}/activate`

Reactiva un paciente previamente desactivado.

#### Headers
```
Authorization: Bearer <token>
```

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "message": "Paciente reactivado exitosamente"
}
```

### 10. Obtener Estadísticas de Pacientes
**GET** `/api/patients/statistics`

Obtiene estadísticas generales de los pacientes.

#### Headers
```
Authorization: Bearer <token>
```

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "data": {
    "total_patients": 100,
    "active_patients": 95,
    "inactive_patients": 5,
    "recent_patients": 10,
    "gender_distribution": {
      "masculino": 45,
      "femenino": 50,
      "otro": 5
    }
  }
}
```

## Códigos de Error

### 400 - Bad Request
```json
{
  "success": false,
  "message": "El campo first_name es requerido",
  "error": "VALIDATION_ERROR"
}
```

### 401 - Unauthorized
```json
{
  "success": false,
  "message": "Token de autenticación requerido",
  "error": "UNAUTHORIZED"
}
```

### 404 - Not Found
```json
{
  "success": false,
  "message": "Paciente no encontrado",
  "error": "PATIENT_NOT_FOUND"
}
```

### 409 - Conflict
```json
{
  "success": false,
  "message": "El DPI ya está registrado",
  "error": "DUPLICATE_DPI"
}
```

### 500 - Internal Server Error
```json
{
  "success": false,
  "message": "Error interno del servidor",
  "error": "INTERNAL_ERROR"
}
```

## Notas Importantes

1. **Autenticación**: Todos los endpoints requieren autenticación mediante token Bearer.
2. **Código de Paciente**: Se genera automáticamente si no se proporciona.
3. **DPI**: Debe ser único en el sistema.
4. **Soft Delete**: Los pacientes se desactivan en lugar de eliminarse físicamente.
5. **Paginación**: Los endpoints de listado incluyen paginación para mejor rendimiento.
6. **Búsqueda**: La búsqueda es case-insensitive y busca en nombre, apellido, código y DPI.
7. **Validación**: Se valida la unicidad del DPI y código de paciente.
8. **Auditoría**: Se registra quién creó cada paciente y cuándo fue modificado.

## Ejemplos de Uso

### Crear un paciente básico
```bash
curl -X POST http://localhost:5000/api/patients \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ana",
    "last_name": "García",
    "phone": "5555-1234",
    "email": "ana.garcia@email.com"
  }'
```

### Buscar pacientes
```bash
curl -X GET "http://localhost:5000/api/patients/search?q=Ana&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Obtener estadísticas
```bash
curl -X GET http://localhost:5000/api/patients/statistics \
  -H "Authorization: Bearer YOUR_TOKEN"
```
