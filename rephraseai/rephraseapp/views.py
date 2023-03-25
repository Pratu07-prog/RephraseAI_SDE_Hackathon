import requests
from django.shortcuts import render

# Create your views here.
def index(request):

    #storing bearer token
    bearer_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhNcHdjdFl4YWlRdWg4Y0M0ejN0UCJ9.eyJpc3MiOiJodHRwczovL2F1dGgucmVwaHJhc2UuYWkvIiwic3ViIjoiYXV0aDB8NjQxZWI3NDBjOWQ4YjNkOWNjODAxMDIzIiwiYXVkIjpbImh0dHBzOi8vZGl5LnJlcGhyYXNlLmFpL2F1dGgwIiwiaHR0cHM6Ly9yZXBocmFzZWFpLXByb2QudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY3OTc1MzYzNCwiZXhwIjoxNjc5ODQwMDM0LCJhenAiOiIzS1U1anZFcVdKQkNVS25QWDI2b25hU1B5M2pKMzBKNCIsInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUgcmVhZDpyZXBocmFzZS5haSBhbGw6ZGl5IHJlYWQ6cmVwaHJhc2UuYWkifQ.WRj1l2jpIEIu_lbetY5tRRsq9M8fZvEksELOdCaI9b2SwUU4tLeyqhgHQXLEoCvCxtBV2Qvag8-QhOnm9lr9kGKQMiRCx2dAyjZsNIIN7m_z1_swn6RGRrsQMWFaN_lbFvYDrqxzN4-xNCq-xSFkregXCwZvQpcbT27GcBwFeWR6WL1spyw2d5DYyCs0pKH1P28-mCRh7NEmI7p29IiWpyVYbGYTK0c3PuNX0ODfU6F1lLZAM4K2Tt-s21vBwLxyPECMG4knaaKK1Fw9Kv5cT_x4O7C2Gzh9Svq6kTTzKHL_caC3SbhqMZ-b1PKm_CW8UL8OoobK5im93GtJyKKHQw"


    if request.POST.get("resume_content"):
        resume_text = request.POST.get("resume_content")
        resume_title = "My resume"
        payload = {
            "videoDimension": {"height": 1080, "width": 1920},
            "scenes": [
                {
                    "elements": [
                        {
                            "style": {
                                "height": "100%",
                                "width": "100%",
                                "position": "absolute",
                                "zIndex": 1,
                            },
                            "asset": {
                                "kind": "Image",
                                "use": "Background",
                                "url": "https://www.musicinminnesota.com/wp-content/uploads/2021/02/Michael-Jackson-live.jpg",
                            },
                        },
                        {
                            "style": {
                                "position": "absolute",
                                "zIndex": 2,
                                "bottom": "0em",
                                "objectFit": "cover",
                                "height": "37.5em",
                                "width": "66.66666666666667em",
                                "left": "16.666666666666664em",
                            },
                            "asset": {
                                "kind": "Spokesperson",
                                "spokespersonVideo": {
                                    "output_params": {
                                        "video": {
                                            "resolution": {"height": 720, "width": 1280},
                                            "background": {"alpha": 0},
                                            "crop": {"preset": "MS"},
                                        }
                                    },
                                    "model": "danielle_pettee_look_2_nt_aug_2022",
                                    "voiceId": "7bc739a4-7abc-46db-bc75-e24b6f899fa9__005",
                                    "gender": "female",
                                    "transcript": "<speak> {}</speak>".format(resume_text),
                                    "transcript_type": "ssml_limited",
                                },
                            },
                        },
                    ]
                },
            ],
            "title": f"{resume_title}",
            # "thumbnailUrl": "https://blog.siriusxm.com/wp-content/uploads/2022/11/MichaelJacksonChannel-1117.jpg",
        }

        
        #create section
        url_create = "https://personalized-brand.api.rephrase.ai/v2/campaign/create"
        headers = {
            "accept": "application/json",
            "Authorization": bearer_token,
            "content-type": "application/json",
        }
        response = requests.post(url_create, json=payload, headers=headers)
        campaign_id = response.json().get('campaign_id')
        print("Created and campaign_id = {}".format(campaign_id))


        # export section

        url_export = f"https://personalized-brand.api.rephrase.ai/v2/campaign/{campaign_id}/export"
        headers = {
            "accept": "application/json",
            "Authorization": bearer_token,
        }
        response = requests.post(url_export, headers=headers)
        print("exported and campaign_id = {}".format(campaign_id))  


        return render(request,"rephraseapp/index.html",{"campaign_id":campaign_id})
    elif request.POST.get("status") is not None:
        #status section
        print("Cheking status")
        campaign_id = request.POST.get('status')
        url_status = f"https://personalized-brand.api.rephrase.ai/v2/campaign/{campaign_id}"
        headers = {
            "accept": "application/json",
            "Authorization": bearer_token
        }
        response = requests.get(url_status, headers=headers)
        print(response.json())
        video_url = response.json().get("video_url")
        status = response.json().get("status")
        print(video_url)

        return render(request,"rephraseapp/index.html",{"campaign_id":campaign_id, "video_url":video_url,"status":status})
    
    return render(request,"rephraseapp/index.html",{})
    


def check_status(reuqest,campaign_id):
    return "hello"