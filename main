<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>심플 감성 MBTI 테스트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background-color: #fdf6f6;
            color: #4a4a4a;
        }
        .pastel-bg-pink { background-color: #ffd8d8; }
        .pastel-bg-blue { background-color: #d8e2ff; }
        .pastel-bg-green { background-color: #d8f3dc; }
        .pastel-bg-yellow { background-color: #fefae0; }
        
        .fade-in {
            animation: fadeIn 0.8s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .btn-option {
            transition: all 0.3s ease;
            border: 1px solid #eee;
        }
        .btn-option:hover {
            transform: translateY(-2px);
            background-color: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        #loading { display: none; }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">

    <div id="app" class="w-full max-w-md bg-white rounded-3xl shadow-sm overflow-hidden p-8 fade-in">
        <!-- Start Screen -->
        <div id="start-screen" class="text-center">
            <div class="mb-6">
                <span class="text-4xl">✨</span>
            </div>
            <h1 class="text-2xl font-medium mb-4">나의 내면의 색깔 찾기</h1>
            <p class="text-gray-500 mb-8 leading-relaxed">12가지 질문을 통해<br>당신의 MBTI와 어울리는 테마를 알아보세요.</p>
            <button onclick="startTest()" class="w-full py-4 bg-pink-100 text-pink-600 rounded-2xl font-medium hover:bg-pink-200 transition-colors">테스트 시작하기</button>
        </div>

        <!-- Quiz Screen -->
        <div id="quiz-screen" class="hidden">
            <div class="mb-8">
                <div class="flex justify-between text-xs text-gray-400 mb-2">
                    <span id="progress-text">1 / 12</span>
                </div>
                <div class="w-full bg-gray-100 h-1.5 rounded-full">
                    <div id="progress-bar" class="bg-pink-200 h-1.5 rounded-full transition-all duration-300" style="width: 8.33%"></div>
                </div>
            </div>
            <h2 id="question" class="text-lg font-medium mb-8 min-h-[60px] leading-snug text-center">질문이 들어갈 자리입니다.</h2>
            <div id="options" class="space-y-3">
                <!-- Options will be injected here -->
            </div>
        </div>

        <!-- Loading Screen -->
        <div id="loading" class="text-center py-12">
            <div class="animate-pulse space-y-4">
                <div class="text-3xl">🎨</div>
                <p class="text-gray-500">당신의 색깔을 분석하는 중...</p>
            </div>
        </div>

        <!-- Result Screen -->
        <div id="result-screen" class="hidden text-center">
            <p class="text-gray-400 text-sm mb-2">당신에게 어울리는 색은</p>
            <h2 id="mbti-result" class="text-4xl font-bold mb-4 text-pink-400 tracking-widest">ENFP</h2>
            <p id="mbti-desc" class="text-gray-600 mb-8 leading-relaxed"></p>
            
            <div class="rounded-2xl overflow-hidden mb-8 shadow-sm border border-gray-50">
                <div id="result-image-container" class="aspect-square bg-gray-50 flex items-center justify-center relative">
                    <img id="result-image" class="w-full h-full object-cover hidden" alt="테마 이미지">
                    <div id="image-loader" class="text-gray-300 flex flex-col items-center">
                         <div class="w-8 h-8 border-4 border-pink-200 border-t-pink-400 rounded-full animate-spin mb-2"></div>
                         <p class="text-xs">테마 이미지를 그리는 중...</p>
                    </div>
                </div>
            </div>
            
            <button onclick="location.reload()" class="w-full py-4 bg-gray-50 text-gray-500 rounded-2xl font-medium hover:bg-gray-100 transition-colors">다시 테스트하기</button>
        </div>
    </div>

    <script type="module">
        const apiKey = ""; // Gemini API Key will be injected

        const questions = [
            { q: "처음 보는 사람들과 함께 있는 파티에서 나는?", a: [{t: "먼저 말을 걸며 분위기를 주도한다", v: "E"}, {t: "조용히 아는 사람 곁에 머문다", v: "I"}]},
            { q: "주말에 시간이 생겼을 때 나는?", a: [{t: "무조건 밖으로 나가서 사람들을 만난다", v: "E"}, {t: "집에서 혼자만의 시간을 즐긴다", v: "I"}]},
            { q: "새로운 일을 시작할 때 나는?", a: [{t: "전체적인 흐름과 가능성을 본다", v: "N"}, {t: "구체적인 정보와 실현 가능성을 본다", v: "S"}]},
            { q: "영화를 볼 때 나는?", a: [{t: "숨겨진 의미나 비유를 생각하며 본다", v: "N"}, {t: "보여지는 상황과 액션에 집중한다", v: "S"}]},
            { q: "친구의 고민 상담을 해줄 때 나는?", a: [{t: "내 일처럼 공감하며 위로해준다", v: "F"}, {t: "현실적인 해결책과 조언을 준다", v: "T"}]},
            { q: "선물을 고를 때 나는?", a: [{t: "상대방의 마음이 담긴 정성을 생각한다", v: "F"}, {t: "상대방에게 정말 필요한 실용성을 생각한다", v: "T"}]},
            { q: "여행 계획을 세울 때 나는?", a: [{t: "시간별로 세부 일정을 꼼꼼하게 짠다", v: "J"}, {t: "큰 틀만 잡고 상황에 맞게 움직인다", v: "P"}]},
            { q: "방 정리를 할 때 나는?", a: [{t: "항상 제자리에 정돈되어 있어야 마음이 편하다", v: "J"}, {t: "어느 정도 어질러져 있어도 신경 쓰지 않는다", v: "P"}]},
            { q: "대화할 때 나는?", a: [{t: "생각나는 대로 즉흥적으로 말하는 편이다", v: "E"}, {t: "머릿속으로 정리한 뒤 말하는 편이다", v: "I"}]},
            { q: "미래에 대해 생각할 때 나는?", a: [{t: "일어나지 않은 일들에 대한 상상을 즐긴다", v: "N"}, {t: "현재 닥친 문제들을 해결하는 데 집중한다", v: "S"}]},
            { q: "비판을 들었을 때 나는?", a: [{t: "감정적으로 상처를 쉽게 받는다", v: "F"}, {t: "객관적인 사실인지 따져본다", v: "T"}]},
            { q: "약속 시간이 정해지면 나는?", a: [{t: "늦지 않게 미리 준비해서 나가는 편이다", v: "J"}, {t: "마지막 순간에 서둘러 나가는 편이다", v: "P"}]}
        ];

        let currentIdx = 0;
        let scores = { E: 0, I: 0, N: 0, S: 0, T: 0, F: 0, J: 0, P: 0 };

        window.startTest = function() {
            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('quiz-screen').classList.remove('hidden');
            showQuestion();
        }

        function showQuestion() {
            const q = questions[currentIdx];
            document.getElementById('question').innerText = q.q;
            document.getElementById('progress-text').innerText = `${currentIdx + 1} / 12`;
            document.getElementById('progress-bar').style.width = `${((currentIdx + 1) / 12) * 100}%`;
            
            const optionsDiv = document.getElementById('options');
            optionsDiv.innerHTML = '';
            q.a.forEach(opt => {
                const btn = document.createElement('button');
                btn.className = "w-full p-4 text-left rounded-2xl btn-option bg-gray-50 hover:bg-white border border-transparent hover:border-pink-100";
                btn.innerText = opt.t;
                btn.onclick = () => handleAnswer(opt.v);
                optionsDiv.appendChild(btn);
            });
        }

        function handleAnswer(val) {
            scores[val]++;
            currentIdx++;
            if (currentIdx < questions.length) {
                showQuestion();
            } else {
                showResult();
            }
        }

        async function showResult() {
            document.getElementById('quiz-screen').classList.add('hidden');
            document.getElementById('loading').style.display = 'block';

            const mbti = (scores.E >= scores.I ? 'E' : 'I') +
                         (scores.N >= scores.S ? 'N' : 'S') +
                         (scores.T >= scores.F ? 'T' : 'F') +
                         (scores.J >= scores.P ? 'J' : 'P');

            const mbtiDescriptions = {
                'ENFP': '자유로운 영혼의 소유자. 매일이 새로운 모험인 당신!',
                'ENFJ': '정의로운 리더. 타인을 따뜻하게 감싸 안는 당신!',
                'ENTP': '뜨거운 논쟁을 즐기는 변론가. 창의적인 혁명가인 당신!',
                'ENTJ': '대담한 전략가. 목표를 향해 달려가는 당신!',
                'ESFP': '자유로운 영혼의 연예인. 삶을 파티처럼 즐기는 당신!',
                'ESFJ': '사교적인 외교관. 타인에게 헌신적인 당신!',
                'ESTP': '모험을 즐기는 사업가. 행동이 앞서는 당신!',
                'ESTJ': '엄격한 관리자. 체계적으로 리드하는 당신!',
                'INFP': '열정적인 중재자. 내면의 목소리에 귀 기울이는 당신!',
                'INFJ': '선의의 옹호자. 통찰력으로 세상을 바라보는 당신!',
                'INTP': '논리적인 사색가. 끊임없이 탐구하는 당신!',
                'INTJ': '용의주도한 전략가. 완벽함을 추구하는 당신!',
                'ISFP': '호기심 많은 예술가. 현재를 소중히 여기는 당신!',
                'ISFJ': '용감한 수호자. 묵묵히 자리를 지키는 당신!',
                'ISTP': '만능 재주꾼. 도구를 자유자재로 다루는 당신!',
                'ISTJ': '청렴결백한 논리주의자. 원칙을 중시하는 당신!'
            };

            document.getElementById('mbti-result').innerText = mbti;
            document.getElementById('mbti-desc').innerText = mbtiDescriptions[mbti];

            document.getElementById('loading').style.display = 'none';
            document.getElementById('result-screen').classList.remove('hidden');

            // Generate Image via Imagen 4
            await generateThemeImage(mbti);
        }

        async function generateThemeImage(mbti) {
            const prompt = `A dreamy, minimal, high-quality pastel theme illustration for an ${mbti} personality. Soft aesthetic, clean composition, artistic and calming. No text.`;
            
            try {
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=${apiKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        instances: [{ prompt: prompt }],
                        parameters: { sampleCount: 1 }
                    })
                });

                const result = await response.json();
                if (result.predictions && result.predictions[0]) {
                    const imageUrl = `data:image/png;base64,${result.predictions[0].bytesBase64Encoded}`;
                    const imgElement = document.getElementById('result-image');
                    imgElement.src = imageUrl;
                    imgElement.classList.remove('hidden');
                    document.getElementById('image-loader').classList.add('hidden');
                }
            } catch (error) {
                console.error("Image generation failed", error);
                document.getElementById('image-loader').innerHTML = '<p class="text-xs text-red-300">이미지를 불러오지 못했습니다.</p>';
            }
        }
    </script>
</body>
</html>
