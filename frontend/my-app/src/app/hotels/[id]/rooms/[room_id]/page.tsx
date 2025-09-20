"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, Typography, Spin, Carousel, Button, Rate, Form, Input, message } from "antd";
import Image from "next/image";
import api from "@/app/apiClient";

const { Title, Paragraph } = Typography;

interface Hotel {
  id: number;
  title: string;
  stars: number;
  address?: string;
}

interface Room {
  id: number;
  title: string;
  photos?: string[];
  price_for_night: number;
  len_beds: number;
  comfort: string;
  hotel_id: number;
}

export default function RoomPage() {
  const { hotel_id, room_id } = useParams();
  const [room, setRoom] = useState<Room | null>(null);
  const [hotel, setHotel] = useState<Hotel | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRoomAndHotel = async () => {
      try {
        // 1. Получаем комнату
        const roomRes = await api.get(`/rooms/${room_id}/`);
        const roomData: Room = roomRes.data;
        setRoom(roomData);

        // 2. Получаем отель по hotel_id комнаты
        if (roomData.hotel_id) {
          const hotelRes = await api.get(`/hotels/${roomData.hotel_id}/`);
          setHotel(hotelRes.data);
        }
      } catch (err) {
        console.error("Ошибка загрузки:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchRoomAndHotel();
  }, [room_id]);

  const handleRegister = async (values: any) => {
    try {
      await api.post("/users/", values);
      message.success("Вы успешно зарегистрированы!");
    } catch (err) {
      console.error("Ошибка регистрации:", err);
      message.error("Ошибка при регистрации");
    }
  };

  if (loading || !room) return <Spin fullscreen />;

  return (
    <div style={{ padding: 24, maxWidth: 800, margin: "0 auto" }}>
      <Card hoverable>
        {/* Фото комнаты */}
        {room.photos && room.photos.length > 0 && (
          <Carousel arrows infinite={false}>
            {room.photos.map((url, index) => (
              <Image
                key={index}
                src={`http://localhost:8000${url}/`}
                alt={`Фото комнаты ${index + 1}`}
                width={800}
                height={500}
                style={{ objectFit: "cover", borderRadius: 8 }}
              />
            ))}
          </Carousel>
        )}

        {/* Инфо об отеле */}
        {hotel && (
          <div style={{ marginTop: 16 }}>
            <Rate disabled defaultValue={hotel.stars || 0} />
            <Title level={3} style={{ marginTop: 8 }}>
              {hotel.title}
            </Title>
            <Paragraph>📍 {hotel.address || "Адрес не указан"}</Paragraph>
          </div>
        )}

        {/* Инфо комнаты */}
        <div style={{ marginTop: 24 }}>
          <Title level={4}>{room.title}</Title>
          <Paragraph>🛏️ Кроватей: {room.len_beds}</Paragraph>
          <Paragraph>✨ Комфорт: {room.comfort}</Paragraph>
          <Paragraph>💰 Цена: {room.price_for_night} ₽ / ночь</Paragraph>
        </div>

      </Card>

      {/* Форма регистрации */}
      <Card hoverable style={{ marginTop: 32 }}>
        <div>
          <Title level={4}>Регистрация для брони</Title>
          <Form layout="vertical" onFinish={handleRegister}>
            <Form.Item
              label="Имя"
              name="first_name"
              rules={[{ required: true, message: "Введите имя" }]}
            >
              <Input placeholder="Ваше имя" />
            </Form.Item>
            <Form.Item
              label="Фамилия"
              name="last_name"
              rules={[{ required: true, message: "Введите фамилию" }]}
            >
              <Input placeholder="Ваша фамилия" />
            </Form.Item>
            <Form.Item
              label="Email"
              name="email"
              rules={[
                { required: true, message: "Введите email" },
                { type: "email", message: "Некорректный email" },
              ]}
            >
              <Input placeholder="you@example.com" />
            </Form.Item>
            <Form.Item
              label="Пароль"
              name="password"
              rules={[{ required: true, message: "Введите пароль" }]}
            >
              <Input.Password placeholder="******" />
            </Form.Item>

            <Button type="primary" htmlType="submit">
              Зарегистрироваться
            </Button>
          </Form>
        </div>
      </Card>
    </div>
  );
}