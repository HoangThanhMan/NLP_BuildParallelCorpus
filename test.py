def align_data(data1, data2, compute_similarity_score):
    """
    Align `text` from data1 with `quocngu` from data2 using dynamic programming.
    
    Args:
    - data1: List of dictionaries with "text".
    - data2: List of dictionaries with "quocngu".
    - compute_similarity_score: Function to compute similarity between two strings.
    
    Returns:
    - List of aligned pairs with their similarity scores.
    """
    m = len(data1)
    n = len(data2)
    
    # Tạo ma trận điểm tương đồng
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    backtrack = [[None] * (n + 1) for _ in range(m + 1)]

    # Điền điểm tương đồng vào ma trận
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            sim_score = compute_similarity_score(data1[i - 1]["text"], data2[j - 1]["quocngu"])
            dp[i][j] = max(
                dp[i - 1][j - 1] + sim_score,  # Match
                dp[i - 1][j],                 # Skip `data1`
                dp[i][j - 1]                  # Skip `data2`
            )

            # Lưu truy vết
            if dp[i][j] == dp[i - 1][j - 1] + sim_score:
                backtrack[i][j] = (i - 1, j - 1)
            elif dp[i][j] == dp[i - 1][j]:
                backtrack[i][j] = (i - 1, j)
            else:
                backtrack[i][j] = (i, j - 1)

    # Truy vết để tìm các cặp dóng hàng
    i, j = m, n
    alignment = []
    while i > 0 and j > 0:
        prev = backtrack[i][j]
        if prev and prev == (i - 1, j - 1):
            alignment.append({
                "text": data1[i - 1]["text"],
                "quocngu": data2[j - 1]["quocngu"],
                "similarity_score": compute_similarity_score(data1[i - 1]["text"], data2[j - 1]["quocngu"])
            })
        i, j = prev if prev else (0, 0)

    # Đảo ngược kết quả để trả về đúng thứ tự
    alignment.reverse()
    return alignment

# Hàm tính điểm tương đồng (cần bạn xử lý)
def compute_similarity_score(text1, text2):
    # Placeholder: điểm tương đồng sẽ do bạn định nghĩa
    return len(set(text1).intersection(set(text2))) / max(len(text1), len(text2))

# Ví dụ dữ liệu
data1 = [
    {"text": "會同四教名師"},
    {"text": "課代德需黎界看景興主鄭要靖都王固扒特台柴奇沒柴方"},
    {"text": "西沒柴本國㩜於儿帮在庫彭欺氏固茹官慭罕注主靖都王"}
]

data2 = [
    {"hannom": "會同四教名師", "quocngu": ""},
    {"hannom": "課代德黎景興。主鄭靖都王固扒特柴奇。沒柴方", "quocngu": "thuở đời đức vua lê là vua cảnh hưng chúa trịnh là tịnh đô vương có bắt được hai thầy cả một thầy phương"},
    {"hannom": "西沒柴本國於几在庫彭。欺衣固茹官注主靖都王", "quocngu": "tây một thầy bản quốc giam ở kẻ chợ tại khố bành khi ấy có nhà quan sáu là chú chúa tịnh đô vương"}
]

# Chạy thử
aligned_results = align_data(data1, data2, compute_similarity_score)
for result in aligned_results:
    print(result)
