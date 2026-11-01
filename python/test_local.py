"""
Local test script - run this without n8n to test the AI qualification.
"""
import json
from qualify_lead import qualify
from crm_writer import save_lead

# Sample leads for testing
test_leads = [
    {
        "name": "Sara Mohammadi",
        "email": "sara@gmail.com",
        "phone": "+989121234567",
        "message": "سلام، قیمت دوره پایتونتون چقدره؟ میخوام همین هفته شروع کنم",
        "budget": "حدود ۳ میلیون",
        "source": "instagram",
    },
    {
        "name": "John Smith",
        "email": "john@company.com",
        "phone": "",
        "message": "Just looking around, send me some info later",
        "budget": "",
        "source": "website",
    },
    {
        "name": "Reza Karimi",
        "email": "reza@outlook.com",
        "phone": "+98935...",
        "message": "I need this urgently for my team. Budget is ready. Call me.",
        "budget": "2000 USD",
        "source": "linkedin",
    },
]

if __name__ == "__main__":
    print("=== AI Lead Qualification Test ===\n")

    for i, lead in enumerate(test_leads, 1):
        print(f"--- Lead #{i}: {lead['name']} ---")
        result = qualify(lead)
        print(f"Score   : {result.get('score')}")
        print(f"Reason  : {result.get('reason')}")
        print(f"Source  : {result.get('source')}")
        print(f"Priority: {result.get('priority')}")

        lead_id = save_lead(lead, result)
        print(f"Saved as Lead ID: {lead_id}\n")

    print("✅ Test finished. Check data/leads.db")