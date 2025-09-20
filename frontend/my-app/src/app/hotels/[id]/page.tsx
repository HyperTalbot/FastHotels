"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Typography, Spin, Card, Button, Rate, Carousel, } from "antd";
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
  comfort: string;
  address?: string;
  photos?: string[]; // относительные пути
}

interface Room {
  id: number;
  photos?: string[];
  title: string;
  price_for_night: number;
  len_beds: number;
  comfort: string;
}


function normalizePhotos(input?: string[] | string | null): string[] {
  if (!input) return [];
  if (Array.isArray(input)) {
    return input.filter((s) => typeof s === "string" && s.trim().length > 0);
  }
  if (typeof input === "string") {
    try {
      const parsed = JSON.parse(input);
      if (Array.isArray(parsed)) {
        return parsed.filter((s) => typeof s === "string" && s.trim().length > 0);
      }
    } catch {
      // не JSON, попробуем разделить по запятой
      return input
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s.length > 0);
    }
  }
  return [];
}


export default function HotelDetailPage() {
  const {id: hotel_id} = useParams();
  const [hotel, setHotel] = useState<Hotel | null>(null);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHotel = async () => {
      try {
        const [hotelRes, roomsRes] = await Promise.all([
          api.get(`/hotels/${hotel_id}/`),
          api.get(`/hotels/${hotel_id}/rooms/`), // список комнат этого отеля
        ]);
        setHotel(hotelRes.data);
        setRooms(roomsRes.data);
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHotel();
  }, [hotel_id]);

  if (loading || !hotel) return <Spin fullscreen />;

  
  return (
    <div style={{ padding: "24px", maxWidth: 1000, margin: "0 auto" }}>
      {/* Карточка отеля  */}
      <div>
        <Card
          hoverable
          title={<><br /><Title level={2}>{hotel.title}</Title></>}
          extra={<Rate disabled defaultValue={hotel.stars} />}
        >
          {hotel.photos && hotel.photos.length > 0 && (
            <Carousel arrows infinite={false}>
              {hotel.photos.map((url, index) => (
                <Image
                  key={index}
                  src={`http://localhost:8000${url}`}
                  alt={`Фото отеля ${index + 1}`}
                  width={600}
                  height={400}
                  style={{ objectFit: "cover", borderRadius: 8 }}
                />
              ))}
            </Carousel>
          )}
          <Paragraph style={{marginTop: 16}}>✨ Удобства: {hotel.comfort}</Paragraph>
          <Paragraph>📍 Адрес: {hotel.address || "Не указан"}</Paragraph>
          <Paragraph>⭐ Рейтинг: {hotel.rating}</Paragraph>
          <Paragraph>💰 Цена: от {hotel.min_price_for_night} ₽ / ночь</Paragraph>

          <Paragraph style={{ marginTop: 32 }}>📜 {hotel.description}</Paragraph>
        </Card>
      </div>

      {/* Даты */}
      <div style={{ marginTop: 15, marginBottom: 15}}>
        <Card hoverable>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <p style={{ margin: 0, textAlign: "left" }}>📅 Заезд: 01.01.2010 </p>
            <p style={{ margin: 0, textAlign: "center" }}>📆 Выезд: 01.01.2010</p>

            <Button type="primary">
              Изменить
            </Button>
          </div>
        </Card>
      </div>

      {/* Список комнат */}
      <div>
        <Card hoverable title={<h2>Доступные варианты</h2>}>
            <Carousel arrows infinite={false} slidesToShow={3} slidesToScroll={1}>
              {rooms.map((room) => {
                const photos = normalizePhotos(room.photos);
                return (
                  <div key={room.id}>
                    <Card
                      hoverable
                      style={{ width: 280 }}
                      title={<Title level={4}>{room.title}</Title>}
                    >
                      {photos.length > 0 ? (
                        <Carousel arrows infinite={false}>
                          {photos.map((url, index) => {
                            const safeUrl = url.startsWith("/") ? url : `/${url}`;
                            return (
                              <Image
                                key={index}
                                alt={`Фото комнаты ${room.title}`}
                                src={`http://localhost:8000${safeUrl}`}
                                width={220}
                                height={160}
                                style={{ objectFit: "cover", borderRadius: 8 }}
                              />
                            );
                          })}
                        </Carousel>
                      ) : (
                        <Image
                          alt="Нет фото"
                          src="/placeholder.jpg"
                          width={220}
                          height={160}
                          style={{ objectFit: "cover", borderRadius: 8 }}
                        />
                      )}
                      <Paragraph>✨ Комфорт: {room.comfort}</Paragraph>
                      <Paragraph>🛏️ Кроватей: {room.len_beds}</Paragraph>
                      <Paragraph>💰 Лучшая цена: {room.price_for_night}</Paragraph>
                      <Button
                        type="primary"
                        style={{ marginTop: 24 }}
                        href={`/hotels/${hotel_id}/rooms/${room.id}/`}
                      >
                        Забронировать
                      </Button>
                    </Card>
                  </div>
                );
              })}
            </Carousel>
        </Card>
      </div>
    </div>
  );
}