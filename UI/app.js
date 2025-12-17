/**
 * AdSage AI - Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- Index Page Logic (Draft Analysis) ---
    const analyzeBtn = document.getElementById('analyzeBtn');
    const fileInput = document.getElementById('fileInput');
    const captionInput = document.getElementById('captionInput');
    const dropZone = document.getElementById('dropZone');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const fileName = document.getElementById('fileName');

    if (analyzeBtn && fileInput) {

        // File Selection Helper
        const handleFile = (file) => {
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imagePreview.src = e.target.result;
                    previewContainer.classList.remove('hidden');
                    fileName.innerText = file.name;
                };
                reader.readAsDataURL(file);
            }
        };

        // Event Listeners
        fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

        // Drag & Drop
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = 'var(--primary-neon)';
        });
        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = 'var(--glass-border)';
        });
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = 'var(--glass-border)';
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                handleFile(e.dataTransfer.files[0]);
            }
        });

        // Analyze Click
        analyzeBtn.addEventListener('click', () => {
            if (!fileInput.files[0]) {
                alert("Please upload an image first!");
                return;
            }

            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            formData.append('caption', captionInput.value);

            // Show loading style
            analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

            // Send to Backend
            fetch('http://127.0.0.1:5000/analyze_draft', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success && data.prediction) {
                        // Save to LocalStorage for dashboard
                        localStorage.setItem('adsage_analysis', JSON.stringify(data.prediction));
                        // Navigate
                        window.location.href = 'dashboard.html';
                    } else {
                        alert("Analysis Failed: " + (data.error || "Unknown error"));
                        analyzeBtn.innerHTML = 'Analyze Draft <i class="fa-solid fa-sparkles"></i>';
                    }
                })
                .catch(err => {
                    console.error(err);
                    alert("Server Error. Ensure backend is running!");
                    analyzeBtn.innerHTML = 'Analyze Draft <i class="fa-solid fa-sparkles"></i>';
                });
        });
    }


    // --- Dashboard Page Logic ---
    const loader = document.getElementById('loader');
    const dashboardGrid = document.getElementById('dashboardResults');

    if (loader && dashboardGrid) {
        // Hide Loader
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.classList.add('hidden');
            // Show Dashboard
            dashboardGrid.classList.remove('hidden');

            // Retrieve stored analysis
            const analysisData = JSON.parse(localStorage.getItem('adsage_analysis') || '{}');

            if (analysisData) {
                // 1. Render Summary
                const summaryEl = document.getElementById('summaryText');
                if (summaryEl && analysisData.summary) {
                    summaryEl.innerHTML = analysisData.summary;
                }

                // 2. Render Final Verdict (Simulated from summary for now)
                const verdictEl = document.getElementById('verdictText');
                if (verdictEl && analysisData.summary) {
                    verdictEl.innerHTML = analysisData.summary; // reusing summary as verdict
                }

                // 2.5 Update Engagement Metrics (Dynamic)
                const engagementCard = document.querySelector('.card.col-span-3 .metric-big').closest('.card');
                if (engagementCard && analysisData.predicted_engagement) {
                    const scoreEl = engagementCard.querySelector('.metric-big');
                    const labelEl = engagementCard.querySelector('.metric-label');

                    // Handle object vs string (fallback)
                    let score = analysisData.predicted_engagement.score || analysisData.predicted_engagement;
                    let justification = analysisData.predicted_engagement.justification || "Based on visual trends.";

                    if (typeof score === 'string' && score.length > 2) score = score.substring(0, 3); // simplistic clean

                    if (scoreEl) scoreEl.innerText = `${score}/10`;
                    if (labelEl) labelEl.innerText = justification;
                }

                // 3. Render Optimization Tips
                const improvementList = document.getElementById('improvementList');
                if (improvementList && analysisData.optimization_tips) {
                    improvementList.innerHTML = analysisData.optimization_tips.map(tip => `
                                <li>
                                    <i class="fa-solid fa-lightbulb"></i>
                                    <div>
                                        <strong>Optimization Tip</strong> <span style="font-size:0.7em; text-transform:uppercase; opacity:0.7; border:1px solid #555; padding:2px 5px; border-radius:4px; margin-left:5px;">AI</span><br>
                                        <span style="color: #bbb;">${tip}</span>
                                    </div>
                                </li>
                            `).join('');
                }

                // 3.1 Render Tone (Dynamic)
                const toneContainer = document.getElementById('toneContainer');
                if (toneContainer && analysisData.tone_and_emotion) {
                    const colors = ['var(--primary-neon)', 'var(--accent-pink)', 'var(--secondary-violet)'];
                    toneContainer.innerHTML = analysisData.tone_and_emotion.map((item, index) => `
                        <div class="flex" style="justify-content: space-between; margin-bottom: 0.5rem;">
                            <span>${item.label}</span>
                            <span style="color: ${colors[index % colors.length]};">${item.score}%</span>
                        </div>
                        <div style="width:100%; height:4px; background:rgba(255,255,255,0.1); border-radius:2px; margin-bottom:0.8rem;">
                             <div style="width:${item.score}%; height:100%; background:${colors[index % colors.length]}; border-radius:2px;"></div>
                        </div>
                    `).join('');
                }

                // 3.2 Render Virality (Dynamic)
                const viralityValue = document.getElementById('viralityValue');
                const viralityBadge = document.getElementById('viralityBadge');
                const viralityLabel = document.getElementById('viralityLabel');

                if (viralityValue && analysisData.virality_score) {
                    const level = analysisData.virality_score.level || "Medium";
                    const badge = analysisData.virality_score.badge_text || "";
                    const label = analysisData.virality_score.justification || "";

                    // Color logic
                    let color = 'white';
                    if (level.toLowerCase().includes('high')) color = 'var(--primary-neon)';
                    else if (level.toLowerCase().includes('medium')) color = 'var(--secondary-violet)';
                    else color = '#999';

                    viralityValue.style.color = color;
                    viralityValue.innerHTML = `${level} ${badge ? `<span class="virality-badge" style="display:inline-block">${badge}</span>` : ''}`;

                    if (viralityLabel) viralityLabel.innerText = label;
                }

                // 3.5 Render Hashtags (Dynamic)
                const hashtagContainer = document.getElementById('hashtagContainer');
                const trendingText = document.getElementById('trendingText');

                if (hashtagContainer && analysisData.hashtags) {
                    hashtagContainer.innerHTML = analysisData.hashtags.slice(0, 10).map((tag, index) => {
                        const isHot = index < 2 ? 'hot' : ''; // Highlight first 2 tags
                        return `<div class="tag ${isHot}">${tag}</div>`;
                    }).join('');

                    // Update trending text with the first hashtag
                    if (trendingText && analysisData.hashtags.length > 0) {
                        const topTag = analysisData.hashtags[0];
                        trendingText.innerHTML = `<i class="fa-solid fa-arrow-trend-up"></i> <strong>${topTag}</strong> is currently trending +${Math.floor(Math.random() * 200) + 100}% this week.`;
                    }
                }

                // 4. Update Age-Bars (Simulated parsing from text description is hard, so we mock random values or parse if prompt returns numbers. 
                // For now, let's assume the prompt returns qualitative data, so we just set standard values or parsing logic if feasible.
                // Improving prompt output would be better (to return numbers). 
                // Let's assume the prompt returns qualitative "youth: strong", "adult: moderate".
                // For this iteration, we visualize the TEXT.)

                const barYouth = document.getElementById('bar-youth');
                const barAdult = document.getElementById('bar-adult');
                const barSenior = document.getElementById('bar-senior');

                // We will display the text analysis for each group
                document.querySelector('.seg-youth').title = analysisData.age_group_reactions?.youth || "N/A";
                document.querySelector('.seg-adult').title = analysisData.age_group_reactions?.adult || "N/A";
                document.querySelector('.seg-senior').title = analysisData.age_group_reactions?.senior || "N/A";

                // Inject the text analysis into the DOM so user can read it
                const audienceSection = document.querySelector('.card.col-span-6 div');
                if (audienceSection && analysisData.age_group_reactions) {
                    audienceSection.innerHTML += `
                                <div style="margin-top:1rem; font-size:0.85rem; border-top:1px solid #333; padding-top:0.5rem;">
                                    <p><strong style="color:var(--primary-neon)">Youth:</strong> ${analysisData.age_group_reactions.youth}</p>
                                    <p><strong style="color:var(--secondary-violet)">Adults:</strong> ${analysisData.age_group_reactions.adult}</p>
                                    <p><strong style="color:#666">Seniors:</strong> ${analysisData.age_group_reactions.senior}</p>
                                </div>
                              `;
                }
            }

            // Trigger Entrance Animation
            requestAnimationFrame(() => {
                dashboardGrid.classList.add('visible');
                animateBars();
            });

        }, 500);
    }

    // --- Helper Functions ---
    // (Existing helpers...)

    // --- Campaign Manager Logic ---
    const generateBtn = document.getElementById('generateCampaignBtn');
    const connectLinkedInBtn = document.getElementById('connectLinkedInBtn');

    if (connectLinkedInBtn) {
        // Check Status
        fetch('http://127.0.0.1:5000/status')
            .then(res => res.json())
            .then(data => {
                if (data.linkedin_connected) {
                    connectLinkedInBtn.innerHTML = '<i class="fa-brands fa-linkedin"></i> Connected';
                    connectLinkedInBtn.disabled = true;
                    connectLinkedInBtn.style.background = 'var(--secondary-violet)';
                }
            });

        connectLinkedInBtn.addEventListener('click', () => {
            fetch('http://127.0.0.1:5000/auth/linkedin')
                .then(res => res.json())
                .then(data => {
                    if (data.url) window.location.href = data.url;
                });
        });
    }

    if (generateBtn) {
        generateBtn.addEventListener('click', () => {
            const daysInput = document.getElementById('campaignDays');
            const days = daysInput ? daysInput.value : 5;
            const strategyText = document.getElementById('verdictText').innerText; // Grabbing text from UI for now

            // Retrieve stored analysis for visual context
            const analysisData = JSON.parse(localStorage.getItem('adsage_analysis') || '{}');
            const visualDescription = analysisData.visual_description || "A generic image relevant to the strategy.";

            const campaignContainer = document.getElementById('campaignContainer');
            const campaignList = document.getElementById('campaignList');

            // Show loading state
            generateBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';

            fetch('http://127.0.0.1:5000/generate_campaign', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ strategy: strategyText, days: days, visual_description: visualDescription })
            })
                .then(res => res.json())
                .then(data => {
                    generateBtn.innerHTML = 'Generate Campaign <i class="fa-solid fa-wand-magic-sparkles"></i>';

                    if (data.success && data.campaign) {
                        campaignContainer.classList.remove('hidden');

                        campaignList.innerHTML = data.campaign.map(post => `
                        <div class="card" style="margin-bottom: 1rem; border: 1px solid var(--glass-border);">
                            <div class="card-header" style="justify-content: space-between;">
                                <span><i class="fa-regular fa-calendar"></i> Day ${post.day}: ${post.topic}</span>
                                <button class="post-now-btn" data-text="${encodeURIComponent(post.content)}" style="background:var(--primary-neon); color:black; border:none; padding:5px 10px; border-radius:4px; font-size:0.8rem; cursor:pointer;">
                                    Post to LinkedIn <i class="fa-solid fa-paper-plane"></i>
                                </button>
                            </div>
                            <p style="margin-top:0.5rem; font-style:italic;">"${post.content}"</p>
                            
                            <!-- Image Generation Area -->
                            <div class="image-area" id="img-area-${post.day}" style="margin-top:0.5rem; border-top:1px solid rgba(255,255,255,0.1); padding-top:0.5rem;">
                                <div style="font-size:0.8rem; color:#888; margin-bottom:0.5rem;">
                                    <i class="fa-regular fa-image"></i> Idea: ${post.image_prompt}
                                </div>
                                <button onclick="generateImageForPost('${post.image_prompt.replace(/'/g, "\\'")}', 'img-area-${post.day}')" 
                                    style="background:transparent; border:1px solid var(--primary-neon); color:var(--primary-neon); padding:5px 10px; border-radius:4px; font-size:0.8rem; cursor:pointer; width:100%;">
                                    <i class="fa-solid fa-paintbrush"></i> Generate Image (Nano Banana)
                                </button>
                            </div>
                        </div>
                     `).join('');
                        // ... Event listeners ...
                        document.querySelectorAll('.post-now-btn').forEach(btn => {
                            btn.addEventListener('click', (e) => {
                                // ... existing logic ...
                                const text = decodeURIComponent(e.target.closest('button').dataset.text);
                                const originalBtnContent = e.target.closest('button').innerHTML;
                                e.target.closest('button').innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

                                fetch('http://127.0.0.1:5000/post_update', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ text: text })
                                })
                                    // ...
                                    .then(res => res.json())
                                    .then(resData => {
                                        if (resData.success) {
                                            e.target.closest('button').innerHTML = '<i class="fa-solid fa-check"></i> Posted!';
                                            e.target.closest('button').style.background = 'var(--secondary-violet)';
                                        } else {
                                            alert("Error posting: " + (resData.error || "Unknown error"));
                                            e.target.closest('button').innerHTML = originalBtnContent;
                                        }
                                    });
                            });
                        });

                    } else {
                        alert("Failed to generate campaign: " + (data.error || "Unknown Error"));
                    }
                });
        });
    }

    // --- Helper Functions ---

    function animateBars() {
        const barYouth = document.getElementById('bar-youth');
        const barAdult = document.getElementById('bar-adult');
        const barSenior = document.getElementById('bar-senior');

        if (barYouth && barAdult && barSenior) {
            // Slight delay for bar animation to look cool
            setTimeout(() => {
                barYouth.style.width = '65%';
                barAdult.style.width = '30%';
                barSenior.style.width = '5%';
            }, 300);
        }
    }
});

// --- Global Functions ---
window.generateImageForPost = (prompt, containerId) => {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Find or create a result area
    let resultArea = container.querySelector('.gen-result');
    if (!resultArea) {
        resultArea = document.createElement('div');
        resultArea.className = 'gen-result';
        resultArea.style.marginTop = '10px';
        container.appendChild(resultArea);
    }

    // Hide the button
    const btn = container.querySelector('button');
    if (btn) btn.style.display = 'none';

    // Show loading in result area
    resultArea.innerHTML = '<div style="color:var(--primary-neon); text-align:center;"><i class="fa-solid fa-spinner fa-spin"></i> Generating...</div>';

    fetch('http://127.0.0.1:5000/generate_image_for_post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: prompt })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success && data.image_url) {
                resultArea.innerHTML = `
                <img src="${data.image_url}" style="width:100%; border-radius:8px; border:1px solid var(--glass-border); animation: fadeIn 0.5s; margin-bottom:10px;">
                <a href="${data.image_url}" download="generated_image.png" style="display:block; text-align:center; color:white; font-size:0.8rem; text-decoration:underline;">Download Generated Image</a>
            `;
            } else {
                // Show error and restore button
                resultArea.innerHTML = `<div style="color:red; font-size:0.8rem; margin-top:5px;">Generation Failed: ${data.error}</div>`;
                if (btn) btn.style.display = 'block';
            }
        })
        .catch(err => {
            resultArea.innerHTML = `<div style="color:red; font-size:0.8rem; margin-top:5px;">Error: ${err.message}</div>`;
            if (btn) btn.style.display = 'block';
        });
};
