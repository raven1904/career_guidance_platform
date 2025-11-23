# Simple test to check URLs
from django.test import TestCase
from django.urls import reverse, resolve
from . import views


class URLTests(TestCase):
    def test_recommendations_dashboard_url(self):
        url = reverse("recommendations:recommendation_dashboard")
        self.assertEqual(resolve(url).func, views.recommendation_dashboard)

    def test_skill_gap_analysis_url(self):
        url = reverse("recommendations:skill_gap_analysis")
        self.assertEqual(resolve(url).func, views.skill_gap_analysis)
