from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from legislators.models import Legislator


class LegislatorPageTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.slug = Legislator.objects.slug

    def test_each_legislator_has_a_page(self):
        """
        Each legislator should have their own page. Sometimes this breaks if
        there are jumpers or if, by some weird chance, two legislators have
        the same name.
        """

        response = self.c.get(reverse('legislator_detail', kwargs={'slug': self.slug}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'legislator.html')
