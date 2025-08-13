'use client';

import { useEffect, useState } from 'react';
import { User } from '@/app/types/user';


export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/users/')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Ошибка при загрузке пользователей:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Загрузка...</p>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Пользователи</h1>
      <ul className="space-y-2">
        {users.map(user => (
          <li key={user.id} className="p-4 bg-gray-100 rounded shadow">
            <p><strong>{user.name}</strong></p>
            <p>{user.email}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}