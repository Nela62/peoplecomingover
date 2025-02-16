"use client";

import { Button } from "./ui/button";
import { toast } from "sonner";

interface ProductCardProps {
  name: string;
  price: number;
  image_url: string;
  placement?: string;
  description: string;
}

export function ProductCard({
  name,
  price,
  image_url,
  placement,
  description,
}: ProductCardProps) {
  const handleOrder = () => {
    toast.success(`${name} added to cart!`);
  };

  return (
    <div className="flex flex-col gap-2 p-4 rounded-xl border bg-card text-card-foreground shadow-sm">
      <div className="aspect-square relative rounded-md overflow-hidden">
        <img
          src={image_url}
          alt={name}
          className="object-cover w-full h-full"
        />
      </div>
      <div className="flex flex-col gap-1">
        <h3 className="font-medium text-sm">{name}</h3>
        <p className="text-sm text-muted-foreground line-clamp-2">
          {description}
        </p>
        {placement && (
          <p className="text-sm text-muted-foreground italic">
            Placement: {placement}
          </p>
        )}
        <div className="flex items-center justify-between mt-2">
          <p className="font-medium">${price.toFixed(2)}</p>
          <Button size="sm" onClick={handleOrder}>
            Order
          </Button>
        </div>
      </div>
    </div>
  );
}
