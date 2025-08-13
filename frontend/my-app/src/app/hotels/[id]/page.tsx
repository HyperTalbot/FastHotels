"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Typography, Spin, Card, Button, Rate } from "antd";
import Image from "next/image";
import api from "@/app/apiClient";

const { Title, Paragraph } = Typography;

interface Hotel {
  id: number;
  title: string;
  description: string;
  min_price_for_night: number;
  rating: number;
  stars: number;
  address?: string;
  photos?: string[]; // относительные пути
}

export default function HotelDetailPage() {
  const { id: hotel_id } = useParams();
  const [hotel, setHotel] = useState<Hotel | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHotel = async () => {
      try {
        const response = await api.get(`/hotels/${hotel_id}`);
        setHotel(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке отеля:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHotel();
  }, [hotel_id]);

  if (loading || !hotel) return <Spin fullscreen />;

  return (
    <div style={{ padding: "24px", maxWidth: 1000, margin: "0 auto" }}>
      <Card
        title={<Title level={2}>{hotel.title}</Title>}
        extra={<Rate disabled defaultValue={hotel.stars} />}
      >
        <Paragraph>📍 Адрес: {hotel.address || "Не указан"}</Paragraph>
        <Paragraph>⭐ Рейтинг: {hotel.rating}</Paragraph>
        <Paragraph>💰 Цена: от {hotel.min_price_for_night} ₽ / ночь</Paragraph>

        {hotel.photos && hotel.photos.length > 0 && (
          <div
            style={{
              display: "flex",
              gap: 16,
              marginTop: 24,
              flexWrap: "wrap",
              justifyContent: "flex-start",
            }}
          >
            {hotel.photos.map((url, index) => (
              <Image
                key={index}
                src={`http://localhost:8000${url}`}
                alt={`Фото отеля ${index + 1}`}
                width={400}
                height={300}
                style={{ objectFit: "cover", borderRadius: 8 }}
              />
            ))}
          </div>
        )}

        <Paragraph style={{ marginTop: 32 }}>{hotel.description}</Paragraph>

        <Button type="primary" style={{ marginTop: 24 }}>
          Забронировать
        </Button>
      </Card>
    </div>
  );
}