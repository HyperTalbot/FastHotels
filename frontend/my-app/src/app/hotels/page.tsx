"use client";

import React, { useEffect, useState } from "react";
import {
  Card,
  Col,
  Row,
  Typography,
  Spin,
  DatePicker,
  Slider,
  Select,
  Form,
  Button,
} from "antd";
import api from "@/app/apiClient";
import Link from "next/link";
import dayjs, { Dayjs } from "dayjs";
import Image from "next/image";

const { Title } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

interface Hotel {
  id: number;
  title: string;
  description: string;
  min_price_for_night: number;
  rating: number;
  stars: number;
  photos?: string[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function HotelsPage() {
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    check_in: null as Dayjs | null,
    check_out: null as Dayjs | null,
    price: [1000, 20000],
    stars: [] as number[],
    sort: "",
  });

  const fetchHotels = async () => {
    setLoading(true);
    try {
      const params: any = {
        min_price: filters.price[0],
        max_price: filters.price[1],
      };

      if (filters.check_in) params.check_in = filters.check_in.format("YYYY-MM-DD");
      if (filters.check_out) params.check_out = filters.check_out.format("YYYY-MM-DD");
      if (filters.stars.length) params.stars = filters.stars.join(",");
      if (filters.sort) params.sort = filters.sort;

      const response = await api.get("/hotels", { params });
      setHotels(response.data);
    } catch (error) {
      console.error("Failed to fetch hotels:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHotels();
  }, []);

  const onFinish = (values: any) => {
    const [check_in, check_out] = values.dates || [];
    setFilters({
      check_in,
      check_out,
      price: values.price,
      stars: values.stars || [],
      sort: values.sort || "",
    });
  };

  useEffect(() => {
    fetchHotels();
  }, [filters]);

  return (
    <div style={{ padding: "24px" }}>
      <Title level={2}>Выбор отеля</Title>

      <Form layout="vertical" onFinish={onFinish} style={{ marginBottom: 24 }}>
        <Row gutter={16}>
          <Col span={6}>
            <Form.Item label="Даты" name="dates">
              <RangePicker style={{ width: "100%" }} format="DD.MM.YYYY" />
            </Form.Item>
          </Col>

          <Col span={6}>
            <Form.Item label="Цена за ночь (₽)" name="price" initialValue={filters.price}>
              <Slider range min={0} max={50000} step={500} tooltip={{ open: true }} />
            </Form.Item>
          </Col>

          <Col span={4}>
            <Form.Item label="Звёзды" name="stars">
              <Select mode="multiple" allowClear placeholder="Количество звёзд">
                {[1, 2, 3, 4, 5].map((s) => (
                  <Option key={s} value={s}>{s}★</Option>
                ))}
              </Select>
            </Form.Item>
          </Col>

          <Col span={4}>
            <Form.Item label="Сортировка" name="sort">
              <Select allowClear placeholder="Сортировать по...">
                <Option value="price_asc">Цена: по возрастанию</Option>
                <Option value="price_desc">Цена: по убыванию</Option>
                <Option value="rating_desc">Рейтинг</Option>
              </Select>
            </Form.Item>
          </Col>

          <Col span={4} style={{ display: "flex", alignItems: "flex-end" }}>
            <Button type="primary" htmlType="submit">
              Применить фильтры
            </Button>
          </Col>
        </Row>
      </Form>

      {loading ? (
        <Spin fullscreen />
      ) : (
        <Row gutter={[16, 16]}>
          {hotels.map((hotel) => (
            <Col span={8} key={hotel.id}>
              <Link href={`/hotels/${hotel.id}`} passHref>
                <Card
                  hoverable
                  title={hotel.title}
                  style={{ height: "100%" }}
                  cover={
                    <Image
                      src={
                        hotel.photos && hotel.photos.length > 0
                          ? `${API_URL}${hotel.photos[0]}`
                          : "/placeholder.jpg"
                      }
                      alt={hotel.title}
                      width={400}
                      height={250}
                      style={{ objectFit: "cover" }}
                    />
                  }
                >
                  <p>{hotel.description.substring(0, 100)}...</p>
                  <p>Рейтинг: {hotel.rating}</p>
                  <p>💰 от {hotel.min_price_for_night} ₽ за ночь</p>
                </Card>
              </Link>
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
}
