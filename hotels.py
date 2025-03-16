from fastapi import Query, APIRouter, Body

from schemas.hotels import HotelPATCH, Hotel

router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2,"title": "Дубай", "name": "dubai"}
]


@router.get("", summary="Получить отели")
def get_hotels(
     id: int | None = Query(None, description="Айдишник"),
     title: str | None = Query(None, description="Название отеля"),
):
 hotels_ = []
 for hotel in hotels:
     if id and hotel["id"] != id:
         continue
     if title and hotel["title"] != title:
         continue
     hotels_.append(hotel)
 return hotels_


@router.delete("/{hotel_id}", summary="Удалить отель по id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"delete": "success"}


@router.post("", summary="Добавить отель")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Сочи отель у моря",
        "name": "sochi_sea"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Дубай 5 звезд",
        "name": "dubai_5_star"
    }}

})):
    hotels.append({
        "id": len(hotels) + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"Success": "True"}


@router.put("/{hotel_id}", summary="Полностью перезаписать данные отеля")
def update_hotel_all_fields(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"Update": "success"}
    return {"Error": "No such hotel"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное перезаписать данные отеля",
    description="Можно отправить name, а можно title")
def update_hotel_field(hotel_id: int, hotel_data: HotelPATCH):

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            return {"Update": "success"}
    return {"Error": "No such hotel"}