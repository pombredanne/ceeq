from multiprocessing import Process, Queue
import socket
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from jira import JIRA, JIRAError
import requests
import time


class ProjectType(models.Model):
    """
    Define the type of project as inbound, outbound, or others
    """
    name = models.CharField(max_length=50, unique=True, default='')

    def __unicode__(self):
        return u"{0}".format(self.name)


class ProjectComponent(models.Model):
    """
    Define standard components and its weight factor for different ProjectType
    """
    project_type = models.ForeignKey(ProjectType)
    name = models.CharField(max_length=50, default='')
    weight = models.IntegerField(default=0)

    class Meta:
        unique_together = (("project_type", "name", "weight"), )

    def __unicode__(self):
        return u"{0}: {1}: {2}".format(self.project_type.name, self.name, self.weight)


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    jira_name = models.CharField(max_length=200)  # name of the related project in JIRA
    jira_version = models.CharField(max_length=200, default='All Versions')  # version of issues in JIRA
    score = models.DecimalField(max_digits=5, decimal_places=2, default=109)
    created = models.DateTimeField('date added', auto_now_add=True)
    modified = models.DateTimeField('date modified', auto_now=True)
    active = models.BooleanField(default=True)  # tracking JIRA projects or not
    complete = models.BooleanField(default=False)  # CEEQ projects complete or not

    project_type = models.ForeignKey(ProjectType, default=1)  # type of project

    #  Domain Testing Characteristics 0-5
    accuracy = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    suitability = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    interoperability = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    functional_security = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    usability = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    accessibility = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])

    #  Technical Testing Characteristics 0-5
    technical_security = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    reliability = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    efficiency = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    maintainability = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    portability = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __unicode__(self):
        return '{0}: {1}'.format(self.name, self.score)

    @property
    def fetch_jira_data(self):
        # ck1 = time.time()
        jira = JIRA(options={'server': 'http://jira.west.com'},
                    basic_auth=(settings.JIRA_API_USERNAME, settings.JIRA_API_PASSWORD))

        try:
            if self.jira_version == 'All Versions':
                data1 = jira.search_issues('project={0}'.format(self.jira_name))
            else:
                data1 = jira.search_issues('project={0}&affectedversion=\'{1}\''.format(self.jira_name, self.jira_version),)
        except JIRAError:
            return 'No JIRA Data'

        total = data1.total
        if total > 1000:
            data1 = {'issues': []}
            for i in range(total / 1000 + 1):
                if self.jira_version == 'All Versions':
                    temp1 = jira.search_issues('project={0}'.format(self.jira_name),
                                               startAt=1000 * i,
                                               maxResults=1000,
                                               fields=settings.JIRA_API_FIELDS,
                                               json_result=True)
                    for item in temp1['issues']:
                        data1['issues'].append(item)
                else:
                    temp1 = jira.search_issues('project={0}&affectedversion=\'{1}\''.format(self.jira_name, self.jira_version),
                                               startAt=1000 * i,
                                               maxResults=1000,
                                               fields=settings.JIRA_API_FIELDS,
                                               json_result=True)
                    for item in temp1['issues']:
                        data1['issues'].append(item)
        else:
            if self.jira_version == 'All Versions':
                data1 = jira.search_issues('project={0}'.format(self.jira_name),
                                           maxResults=total,
                                           fields=settings.JIRA_API_FIELDS,
                                           json_result=True)
            else:
                data1 = jira.search_issues('project={0}&affectedversion=\'{1}\''.format(self.jira_name, self.jira_version),
                                           maxResults=total,
                                           fields=settings.JIRA_API_FIELDS,
                                           json_result=True)

        return data1
        # ck2 = time.time()
        #
        # if self.jira_version == 'All Versions':
        #     data = requests.get(settings.JIRA_API_URL_TOTAL_JIRAS + self.jira_name,
        #                         proxies=settings.JIRA_PROXY,
        #                         auth=(settings.JIRA_API_USERNAME, settings.JIRA_API_PASSWORD)).json()
        # else:
        #     data = requests.get(settings.JIRA_API_URL_TOTAL_JIRAS + self.jira_name + '%20AND%20affectedversion=\'' + self.jira_version + '\'',
        #                         proxies=settings.JIRA_PROXY,
        #                         auth=(settings.JIRA_API_USERNAME, settings.JIRA_API_PASSWORD)).json()
        # # print 'total: ', data['total']
        # if len(data) == 2:
        #     if data['errorMessages']:
        #         return 'No JIRA Data'
        # else:
        #     if socket.gethostname() == 'OM1960L1':
        #         return data
        #     else:
        #         def worker(start, que):
        #             if self.jira_version == 'All Versions':
        #                 data_single = requests.get(settings.JIRA_API_URL % (settings.JIRA_API_FIELDS, 50, start, self.jira_name) + '&expand=names',
        #                                            proxies=settings.JIRA_PROXY,
        #                                            auth=(settings.JIRA_API_USERNAME, settings.JIRA_API_PASSWORD)).json()
        #
        #             else:
        #                 data_single = requests.get(settings.JIRA_API_URL % (settings.JIRA_API_FIELDS, 50, start, self.jira_name) + '%20AND%20affectedversion=\'' + self.jira_version +'\'&expand=names',
        #                                            proxies=settings.JIRA_PROXY,
        #                                            auth=(settings.JIRA_API_USERNAME, settings.JIRA_API_PASSWORD)).json()
        #             que.put(data_single)
        #             #data_total.append(data_single['issues'])
        #         jobs = []
        #         queue = Queue()
        #         processes = data['total'] / 50 + 1
        #         issues = []
        #         results = {}
        #
        #         for i in range(processes):
        #             process = Process(target=worker, args=(i * 50, queue,))
        #             jobs.append(processes)
        #             process.start()
        #             for item in queue.get()['issues']:
        #                 issues.append(item)
        #             process.join()
        #
        #         ck3 = time.time()
        #         print ck2 - ck1, ck3 - ck2
        #         results['issues'] = issues
        #         return results

    @property
    def fectch_jira_versions(self):
        versions = []
        data = requests.get(settings.JIRA_API_URL_VERSIONS % self.jira_name.upper(),
                            proxies=settings.JIRA_PROXY,
                            auth=(settings.JIRA_API_USERNAME, settings.JIRA_API_PASSWORD)).json()

        try:
            if data['errorMessages']:
                return 'No JIRA Project'
        except TypeError:
            pass

        for item in data:
            versions.append(item['name'])

        versions.append('All Versions')

        return versions

    @property
    def frame_components(self):
        frame_components = {}
        components = ProjectComponent.objects.filter(project_type=self.project_type)
        for component in components:
            frame_components[str(component.name)] = component.weight

        return frame_components


class ProjectComponentsDefectsDensity(models.Model):
    project = models.ForeignKey(Project)
    version = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    # log ceeq score per day per version
    ceeq = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    # ceeq score disregard JIRA status
    ceeq_closed = models.DecimalField(max_digits=5, decimal_places=3, default=10)

    cxp = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    platform = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    reports = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    application = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    voice_slots = models.DecimalField(max_digits=5, decimal_places=3, default=0)

    def __unicode__(self):
        return '{0}: {1}'.format(self.project.name, self.version)

    class Meta:
        #unique_together = (("project", "created", "version"),)
        ordering = ['created', 'version']


class FrameworkParameter(models.Model):
    #  Store framework parameters: jira_issue_weight_sum, vaf_ratio, vaf_exp
    parameter = models.CharField(max_length=200, unique=True)
    value = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __unicode__(self):
        return '{0}: {1}'.format(self.parameter, self.value)


