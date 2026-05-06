from google_play_reviews import collect_reviews
from sheets import append_rows


def main():
    print("구글 리뷰 수집 시작")

    all_rows, pos, neg, neu = collect_reviews()

    print(f"전체: {len(all_rows)}")
    print(f"긍정: {len(pos)} / 부정: {len(neg)} / 중립: {len(neu)}")

    append_rows("구글플레이 리뷰", all_rows)
    append_rows("구글플레이 긍정", pos)
    append_rows("구글플레이 부정", neg)
    append_rows("구글플레이 중립", neu)

    print("저장 완료")


if __name__ == "__main__":
    main()
